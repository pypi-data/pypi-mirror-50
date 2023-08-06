//
//  bp_infer.cpp
//  Mod_BP_Xcode
//
//  Created by Benjamin Walker on 5/2/18.
//  Copyright © 2018 Benjamin Walker. All rights reserved.
//

#include "bp_infer.h"
#include <vector>
#include <set>
#include <random>
#include <assert.h>
#include <math.h>
#include <stack>
#include <map>
#include <unordered_set>
using namespace std;


double truncate(const double in, const int q);


BP_Inference::BP_Inference(const vector<index_t>& _layer_membership, const vector<pair<index_t,index_t> > &intra_edgelist, const vector<pair<index_t,index_t> > &inter_edgelist, const index_t _n, const index_t _nt, const int _q, const double _beta, const double _omega, const double _resgamma, bool _verbose, bool _transform) :  layer_membership(_layer_membership), neighbor_count(_n), theta(_nt), num_edges(_nt), n(_n), nt(_nt), q(_q), verbose(_verbose), transform(_transform), order(_n), rng(time(NULL))
{
    eps = 1e-8;
    computed_marginals = false;
    typedef pair<index_t, bool> ibpair;
    vector<vector< ibpair > > edges(n);
    uniform_real_distribution<double> pdist(0,1);
    uniform_int_distribution<index_t> destdist(0,n-1);
    neighbor_offset_map.resize(n);
    total_edges = 0;
    
    // TODO: go through all input edges and put them into the data structure along with categorization of their edge type
    
    
    for (auto p : intra_edgelist)
    {
        index_t i = p.first;
        index_t j = p.second;
        edges[i].push_back(ibpair(j,true));
        edges[j].push_back(ibpair(i,true));
        
        num_edges[layer_membership[i]] += 2;
        total_edges += 2;
    }
    
    /*for (auto p : inter_edgelist)
     {
     index_t i = p.first;
     index_t j = p.second;
     edges[i].push_back(ibpair(j,false));
     edges[j].push_back(ibpair(i,false));
     total_edges += 2;
     }*/
    
    beliefs.resize(q*total_edges);
    beliefs_old.resize(q*total_edges);
    beliefs_offsets.resize(n+1);
    beliefs_temporal.resize(q*n*(nt-1));
    
    neighbors.resize(total_edges);
    neighbors_reversed.resize(total_edges);
    neighbors_offsets.resize(n+1);
    neighbors_type.resize(total_edges);
    
    marginals.resize(q*n);
    marginals_old.resize(q*n);
    
    // set up offsets for fast access and copy graph structure into neighbors array
    size_t neighbors_offset_count = 0;
    size_t beliefs_offset_count = 0;
    int neighbor_c = 0;
    
    beliefs_offsets[0] = 0;
    neighbors_offsets[0] = 0;
    max_degree = 0;
    for (index_t i=0;i<n;++i)
    {
        beliefs_offset_count += q*edges[i].size();
        neighbors_offset_count += edges[i].size();
        neighbor_count[i] = (index_t) edges[i].size();
        
        beliefs_offsets[i+1] = beliefs_offset_count;
        neighbors_offsets[i+1] = neighbors_offset_count;
        
        max_degree = max(max_degree,(index_t) edges[i].size());
        
        for (index_t j=0;j<edges[i].size();++j)
        {
            //assert(neighbor_c < num_edges);
            neighbors_type[neighbor_c] = edges[i][j].second;
            neighbors[neighbor_c++] = edges[i][j].first;
            neighbor_offset_map[i][edges[i][j].first] = j;
        }
    }
    scratch.resize(max_degree*q);
    neighbor_c = 0;
    for (int i=0;i<n;++i)
    {
        for (int j=0;j<edges[i].size();++j)
        {
            neighbors_reversed[neighbor_c++] = neighbor_offset_map[edges[i][j].first][i];
        }
    }
    
    reinit();
    
    compute_bfe = false;
}

long BP_Inference::run(unsigned long maxIters)
{
    
    change = 1;
    //unsigned long maxIters = 100;
    bool converged = false;
    for (unsigned long iter = 0; iter < maxIters; ++iter)
    {
        step();
        
        // monitor changes
        
        
        if (verbose)
            printf("Iteration %lu: change %f\n",iter+1,change);
        
        if (!changed)
        {
            converged = true;
            
            if (verbose)
                printf("Converged after %lu iterations.\n",iter+1);
            
            return iter;
        }
    }
    if (verbose)
        printf("Algorithm failed to converge after %lu iterations.\n",maxIters);
    return maxIters+1;
    
    
}

void BP_Inference::compute_marginal(index_t i, bool do_bfe_contribution)
{
    const index_t nn = neighbor_count[i];
    index_t t = layer_membership[i];
    // iterate over all states
    double Z = 0;

    for (int s = 0; s < q;++s)
    {
        // incoming beliefs are already stored locally
        // figure out the sum of logs part of the update equation that uses the incoming beliefs
        marginals[q*i+s]=1;
        for (index_t idx2 = 0;idx2<nn;++idx2)
        {
            
            double mul = lambda*beliefs[beliefs_offsets[i]+nn*s+idx2] + (1-lambda)/q;
            
            marginals[q*i+s] *= mul;
        }
        // evaluate the rest of the update equation
        marginals[q*i+s]= exp(-theta[t][s]) * marginals[q*i+s] * (eta*beliefs_temporal[i+s]+ (1-eta)/q) * (eta*beliefs_temporal[i - n/nt+s] + (1-eta)/q);
        
        
        Z += marginals[q*i+s];
    }

    // normalize
    for (index_t s = 0; s < q; ++s)
    {
        marginals[q*i + s] /= Z;
        
    }
}

void BP_Inference::step()
{
    changed = false;
    change = 0;
    
    if (compute_bfe)
    {
        bfe = 0.0;
    }
    
    // go through each node and update beliefs
    for (index_t node_idx = 0;node_idx<n;++node_idx)
    {
        index_t i = node_idx;
        index_t t = layer_membership[i];
        const index_t nn = neighbor_count[i];
        if (nn==0) continue;
        
        // first, see how much change we had to incoming beliefs so we know if we need to update
        double local_change = 0;
        for (index_t idx=beliefs_offsets[i];idx<beliefs_offsets[i+1];++idx)
        {
            local_change += fabs(beliefs[idx] - beliefs_old[idx]);
        }
        local_change /= q*nn;
        if (local_change < eps)
        {
            // not enough change in incoming beliefs to warrant an update
            continue;
        }
        // if we changed any nodes, set this to true so we know we haven't converged
        changed = true;
        change += local_change;
        
        // we should update the nodes contribution to theta
        compute_marginal(i);
        for (index_t s = 0; s < q; ++s)
        {
            theta[t][s] += (double(nt)/n) * (marginals[q*i + s] - marginals_old[q*i + s]);
        }
        
        // update our record of what our incoming beliefs were for future comparison
        copy(beliefs.begin()+beliefs_offsets[i],beliefs.begin()+beliefs_offsets[i]+q*nn,beliefs_old.begin()+beliefs_offsets[i]);
        // do the same for marginals
        copy(marginals.begin() + q*i, marginals.begin() + q*i + q, marginals_old.begin() + q*i);
        
        // iterate over all states
        vector<double> tempMessages(q);
        for (int s = 0; s < q;++s)
        {
            // incoming beliefs are already stored locally
            // figure out the sum of logs part of the update equation that uses the incoming beliefs
            tempMessages[s] = 1;
            for (index_t idx=0; idx<nn; ++idx)
            {
                scratch[nn*s+idx] = 0;
                for (index_t idx2 = 0;idx2<nn;++idx2)
                {
                    if (idx2 == idx) continue;
                    
                    double mul = lambda*beliefs[beliefs_offsets[i]+nn*s+idx2] + (1-lambda)/q;
                    
                    scratch[nn*s+idx] *= mul;
                }
                // evaluate the rest of the update equation
                scratch[nn*s+idx] = exp(-theta[t][s]) * scratch[nn*s+idx] * (eta*beliefs_temporal[i+s]+ (1-eta)/q) * (eta*beliefs_temporal[i - n/nt+s] + (1-eta)/q);
                
                
                tempMessages[s] *= lambda*beliefs[beliefs_offsets[i]+nn*s+idx] + (1-lambda)/q;
            }
            tempMessages[s] *= exp(-theta[t][s]) *(1-eta)/q * (eta*beliefs_temporal[i - n/nt+s]);
        }
        
        // normalize the scratch space
        double sum=0;
        for (index_t s=0;s<q;++s)
        {
            sum += tempMessages[s];
        }
        for (index_t s=0;s<q;++s)
        {
            tempMessages[s] /= sum;
        }
        
        for (index_t idx = 0;idx<nn;++idx)
        {
            // iterate over all states
            double sum = 0;
            for (size_t s = 0; s < q;++s)
            {
                sum += scratch[nn*s+idx];
            }
            if (compute_bfe)
            {
                bfe -= log(sum);
            }
            if (sum > 0)
            {
                for (size_t s = 0; s < q;++s)
                {
                    scratch[nn*s+idx] /= sum;
                }
            }
            else
            {
                for (size_t s = 0; s < q;++s)
                {
                    scratch[nn*s+idx] = 1.0/q;
                }
            }
        }
        
        // write the scratch space out to non-local memory
        for (size_t s = 0; s < q; ++s)
        {
            for (index_t idx = 0; idx < nn; ++ idx)
            {
                index_t k = neighbors[neighbors_offsets[i]+idx];
                const index_t nnk = neighbor_count[k];
                index_t idx_out = neighbors_reversed[neighbors_offsets[i]+idx];
                
                beliefs[beliefs_offsets[k]+nnk*s+idx_out] = scratch[nn*s+idx];
            }
            beliefs_temporal[i+s] = tempMessages[s];
        }
    }
    /*
     if (compute_bfe)
     {
     compute_marginals(true);
     
     for (index_t t=0;t<nt;++t)
     {
     double temp = 0;
     for (index_t s=0;s<q;++s)
     {
     double temp2 = theta[t][s];
     temp += temp2*temp2;
     }
     bfe += beta/(2*num_edges[t]) * temp;
     }
     bfe /= (beta*n);
     }
     */
}

void BP_Inference::normalize(vector<double> & beliefs, index_t i)
{
    const index_t nn = neighbor_count[i];
    // iterate over all neighbors
    for (size_t idx2 = 0; idx2 < nn; ++ idx2)
    {
        // iterate over all states
        double sum = 0;
        for (size_t s = 0; s < q;++s)
        {
            sum += beliefs[beliefs_offsets[i]+nn*s+idx2];
        }
        for (size_t s = 0; s < q;++s)
        {
            beliefs[beliefs_offsets[i]+nn*s+idx2] /= sum;
        }
    }
}

void BP_Inference::compute_marginals()
{
    compute_marginals(false);
}

void BP_Inference::compute_marginals(bool do_bfe_contribution)
{
    for (index_t i = 0; i < n; ++i)
    {
        compute_marginal(i,do_bfe_contribution);
    }
}




double BP_Inference::compute_bethe_free_energy()
{
    // - 1/(n*beta) ( sum_i {log Z_i} - sum_{i,j \in E} log Z_{ij} + beta/4m \sum_s theta_s^2 )
    if (compute_bfe == false)
    {
        compute_bfe = true;
        step();
        compute_bfe = false;
    }
    return bfe;
}

double BP_Inference::compute_factorized_free_energy()
{
    //Calculate the bethe free energy of the factorized state ( each node uniform on all communities)
    //log(1-1/q-exp(beta))
    
    //double bffe=log(1-1.0/q - exp(beta));
    return 0;
}


vector<vector<double> > BP_Inference::return_marginals() {
    // make sure the marginals are up-to-date
    compute_marginals();
    
    vector<vector<double> > ret(n);
    
    for (index_t i=0;i<n;++i)
    {
        ret[i].resize(q);
        for (index_t s=0;s<q;++s)
        {
            ret[i][s] = marginals[q*i+s];
        }
    }
    
    return ret;
}



void BP_Inference::setq(double new_q) {
    // rearrange the optimizer to have a different q and reinitialize
    q = new_q;
    
    
    beliefs.resize(q*total_edges);
    beliefs_old.clear();
    beliefs_old.resize(q*total_edges);
    marginals.resize(q*n);
    marginals_old.resize(q*n);
    scratch.resize(q*max_degree);
    
    // regenerate the beliefs_offsets
    index_t offset_count = 0;
    for (index_t i = 0; i<n;++i)
    {
        offset_count += q*neighbor_count[i];
        beliefs_offsets[i+1] = offset_count;
    }
    
    reinit();
    
}

void BP_Inference::reinit(bool init_beliefs,bool init_theta)
{
    if (init_beliefs)
        initializeBeliefs();
    if (init_theta)
        initializeTheta();
    copy(marginals.begin(),marginals.end(), marginals_old.begin());
}

void BP_Inference::initializeBeliefs() {
    // set starting value of beliefs
    // generate values for each state and then normalize
    normal_distribution<double> eps_dist(0,0.1);
    for (size_t idx = 0;idx<q*total_edges;++idx)
    {
        double val = eps_dist(rng);
        beliefs[idx] = truncate(1.0/q + val,q);
    }
    
    for (index_t idx = 0; idx < beliefs_temporal.size();++idx)
    {
        double val = eps_dist(rng);
        beliefs_temporal[idx] = truncate(1.0/q + val,q);
    }
    
    for (index_t i=0;i<n;++i)
    {
        normalize(beliefs,i);
    }
    
    // zero out old beliefs
    for (size_t i=0;i<q*total_edges;++i)
    {
        beliefs_old[i] = 0;
    }
}

void BP_Inference::initializeTheta() {
    // initialize values of theta for each layer
    theta.resize(nt);
    for (index_t t = 0; t < nt; ++t)
    {
        // make sure the size is correct
        theta[t].resize(q);
        for (index_t s = 0; s<q;++s)
        {
            //theta[t][s] = beta*resgamma/(q);
            theta[t][s] = 0;
        }
    }
    
    compute_marginals();
    for (index_t t = 0; t < nt; ++t)
    {
        for (index_t s=0;s<q;++s)
        {
            theta[t][s]=0;
        }
    }
    for (index_t i=0;i<n;++i)
    {
        index_t t = layer_membership[i];
        index_t nn = neighbor_count[i];
        for (index_t s = 0; s<q;++s)
        {
            theta[t][s] += lambda*marginals[q*i + s] + (1-lambda)/q;
        }
    }
    for (int t=0;t<nt;++t)
    {
        for (int s=0;s<q;++s)
        {
            theta[t][s] *= double(nt)/n;
        }
    }
}

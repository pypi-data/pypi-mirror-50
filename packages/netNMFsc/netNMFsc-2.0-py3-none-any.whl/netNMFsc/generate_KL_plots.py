import os,sys
import numpy as np
import netNMFsc
import seaborn as sns
import pandas as pd
import matplotlib
print('matplotlib: '+matplotlib.__version__)
import matplotlib.pyplot as plt
%matplotlib inline


import collections
import random
import copy
from scipy import sparse, io
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.metrics.cluster import adjusted_rand_score
def double_exp_dropout(data,dropout_constant):
    print('applying dropout...')
    genes,cells = data.shape
    newdata = np.zeros([genes,cells])
    dropout = 0
    for i in range(genes):
        for j in range(cells):
            if data[i,j] > 0:
                val = np.log(data[i,j]+1)
            else:
                val = 0
            dropout_rate = np.exp(-dropout_constant*val**2)
            if np.random.binomial(1,dropout_rate):
                newdata[i,j] = 0
                dropout += 1
            else :
                newdata[i,j] = np.exp(val)
    print('dropout rate',dropout / float(data.size))
    return newdata

def mixture_dropout(data,dropout_constant):
    print('applying dropout...')
    data = data.astype(int)
    total_counts = np.sum(data)
    inds = []
    probs = []
    total = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            probs.append(data[i,j])
            inds.append([i,j])
            total += data[i,j]
    probs = list(np.asarray(probs)/float(total))
    downsampled = total * dropout_constant
    p = np.random.multinomial(downsampled, probs)
    dropout = sum([1 for x in p if x == 0])
    print('dropout is',dropout/float(data.size))
    for index,elem in enumerate(inds):
        i,j = elem
        data[i,j] = p[index]
    return data

# K, dropout_constant, edges, network, outdir
def simulate(cluster_sizes,dropout_constant,edges,network,outdir):
    K = len(cluster_sizes)
    print('simulating data...')
    # 1000 cells 5000 genes, 6 clusters, sizes: 300,250,200,100,100,50
    cells = 1000
    genes = 2500
    genenames = [i for i in range(genes)]
    data = np.zeros([genes,cells])
    clusters = K
    #network = np.load(os.path.join(args.network,'network.npy'))

    edges = 0
    overexpressed_genes_per_cluster = collections.defaultdict(list)
    valid_seeds = range(genes)
    for cluster in range(clusters):
        over_expressed_genes = random.sample(genenames,50)
        overexpressed_genes_per_cluster[cluster] = over_expressed_genes

    cluster_assignment = collections.defaultdict(int)
    s = 0
    true_clusters = [0 for i in range(cells)]
    for i in range(len(cluster_sizes)):
        for cell in range(cells):
            if cell >= s and cell < s + cluster_sizes[i]:
                cluster_assignment[cell] = i
                true_clusters[cell] = i
        s += cluster_sizes[i]
    gene_means = [min(8,x) for x in np.random.gamma(1.8,1,genes)]
    for i,gene_mean in enumerate(gene_means):
        #print('gene',i,'with mean',gene_mean)
        entries = []
        for cell in range(cells):
            multiplier = 1.0
            overexpressed_genes = overexpressed_genes_per_cluster[cluster_assignment[cell]]
            if i in overexpressed_genes:
                multiplier = np.random.uniform(1.3,3.0)
            entry = np.random.negative_binomial(1*(np.exp(gene_mean)*multiplier),.5)
            while entry < 0:
                entry = np.random.negative_binomial(1*(np.exp(gene_mean)*multiplier),.5)
            entries.append(np.log(entry+1))
        data[i,:] = np.asarray(entries)
    data = np.exp(data)

    c = np.corrcoef(data)
    c[c<.1]=0
    corr = np.zeros([data.shape[0],data.shape[0]])

    for i in range(clusters):
        for gene in overexpressed_genes_per_cluster[i]:
            for gene2 in overexpressed_genes_per_cluster[i]:
                corr[gene,gene2] = 1.0
                corr[gene2,gene] = 1.0

    corr = c            
    print('before',np.count_nonzero(corr))
    corr = corr 
    print('after',np.count_nonzero(corr))
    #corr[corr<1]=0
    overlap = c[corr!=0]
    overlap = overlap[overlap!=0]
    print('percent network covered by data',len(overlap)/float(len(corr[corr!=0])))
    print('percent data covered by network',len(overlap)/float(len(c[c!=0])))
    print('CORRELATION',corr.shape,np.sum(corr))

    data_drop = mixture_dropout(copy.deepcopy(data),dropout_constant) # perform dropout
    genenames = [str(i) for i in range(genes)]
    for gene1 in overexpressed_genes_per_cluster[0][0:3]:
        for gene2 in overexpressed_genes_per_cluster[0][0:3]:
            print(gene1,gene2,corr[gene1,gene2])
    print(corr)
    return data_drop,list(true_clusters),data,genenames,corr



import time
from scipy import sparse,io
from sklearn.decomposition import NMF

n_inits = 1
max_iter = 5000
n_jobs = 1
tol=1e-4
dropout_constants = [0.020,.045,0.06]
edges = 10000
network = '/n/fs/ragr-data/users/relyanow/scRNA/simulated'
outdir = '/n/fs/ragr-data/users/relyanow/scRNA/simulated'
c = [[333,333,334]]#,[500,200,150,100,50],[500,200,100,100,50,25,25]]
def append_ARI(alpha,ari,num_clusters,H,true_clusters):
    clusterer = KMeans(n_clusters=num_clusters)
    result_clusters = clusterer.fit_predict( H.T)
    ARI = adjusted_rand_score(result_clusters,list(true_clusters))
    ari.append(ARI)
    print('ALPHA',alpha,ARI)
    return ari
    
for d,cluster_sizes in enumerate(c):
    dropout_constant = dropout_constants[d]
    ARI_1 = []
    ARI_5 = []
    ARI_10 = []
    ARI_20 = []
    ARI_30 = []
    ARI_50 = []
    ARI_100 = []
    ARI_0 = []
    ARI_1000 = []
    ARI_10000 = []
    #aris = [ARI_1,ARI_5,ARI_10,ARI_20,ARI_50,ARI_100,ARI_200,ARI_500,ARI_1000,ARI_10000]
    aris = [ARI_0,ARI_1]
    #alphas = [0,0.00001,.0001,.0005,.001,.005,.010,.05,1,10]
    alphas = [.05,.1,.5,1,2,3,5]
    num_clusters = len(cluster_sizes)
    dimensions = 10
    
    for i in range(1):
    
        for a,alpha in enumerate(alphas):
            for j in range(5):
                s = '''matlab -r "run_GNMF_KL %s %s %s %s"'''%(fea_file, network_file, str(dimensions), str(alpha))
                print(s)
                os.system(s)
                H = io.loadmat('/n/fs/ragr-data/users/relyanow/scRNA/simulated/H.mat')['U']
                H = H.T
                aris[a] = append_ARI(alpha,aris[a],num_clusters,H,true_clusters)
            
print(aris)



data = dict()
data['Lambda'] = []
data['ARI'] = []
 
for i,ari in enumerate(aris):    
    alpha = alphas[i]
    for elem in ari:
        data['Lambda'].append(alpha)
        data['ARI'].append(elem)



ax = sns.violinplot(x="Lambda", y="ARI", data=data)
ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
plt.ylim([0.0,1.0])
plt.savefig('/n/fs/ragr-research/projects/scRNA/figures/netNMF_KL_Lambda_crossvalidation_1.pdf', bbox_inches='tight', pad_inches=0.02)


import networkx as nx
import time
import sys

import numpy as np
import pandas as pd

from util.graph_helper import load_graph
from util.graph_helper import load_graph_sample
from util.graph_helper import random_walk_sampling

import algorithms.metrics as Metrics
from algorithms.LPA import LPA
from algorithms.GN import GN
from algorithms.CPM import CPM
from algorithms.Louvain import Louvain

def result_metrics(G, communities, duration, name='keke'):
    print('\n[{}] Algorithm\n'.format(name))
    print('Execution Duration: {}'.format(duration))
    print('Number of Communities: {}'.format(len(communities)))

    ied = []
    ex = []
    cr = []
    cond = []

    coms = []
    for cs in communities:
        if len(cs) > 1:
            community = G.subgraph(cs)
            coms.append(community)
            ied.append(Metrics.internal_density(community))
            ex.append(Metrics.expansion(G, community))
            cr.append(Metrics.cut_ratio(G, community))
            cond.append(Metrics.conductance(G, community))

    m1 = [
        ["Internal Density", min(ied), max(ied), np.mean(ied), np.std(ied)],
        ["Expansion", min(ex), max(ex), np.mean(ex), np.std(ex)],
        ["Cut Ratio", min(cr), max(cr), np.mean(cr), np.std(cr)],
        ["Conductance", min(cond), max(cond), np.mean(cond), np.std(cond)]
    ]

    df = pd.DataFrame(m1, columns=["Index", "min", "max", "avg", "std"])
    df.set_index('Index', inplace=True)

    print(df)

    print('Modularity: {}'.format(Metrics.modularity(G, communities)))
    print('Modularity Gai: {}'.format(Metrics.modularity_gai(G, communities)))

if __name__ == '__main__':
    path_list = ['../../Dataset/facebook/facebook_combined.txt']
    graph_path = path_list[0]
    # G = load_graph(graph_path)

    # sampling
    rate = 0.1
    # G = load_graph_sample(graph_path, rate=rate)
    G = random_walk_sampling(graph_path, rate=rate, metropolized=True)

    print("%d nodes, %d edges" % (len(G.nodes()), len(G.edges())))


    start_time = time.time()

    communities = []

    al = 3
    name = 'keke'
    if al == 0:
        algorithm = GN(G)
        communities = algorithm.execute()
        name = 'GN'
    elif al == 1:
        algorithm = CPM(G)
        communities = algorithm.execute()
        name = 'CPM'
    elif al == 2:
        algorithm = LPA(G)
        communities = algorithm.execute()
        name = 'LPA'
    elif al == 3:
        pyl = Louvain(G)
        communities, q = pyl.execute()
        print('Louvain Modularity: {}'.format(q))
        name = 'Louvain'


    execution_time = (time.time() - start_time)
    time_length = '{0:.2f} s'.format(execution_time)

    result_metrics(G, communities, time_length, name)
    print('Modularity Gai: {}'.format(Metrics.modularity_gai(G, communities)))


import networkx as nx

import sys

from util.graph_helper import load_graph, load_graph_sample
from util.graph_helper import clone_graph
from util.modularity import cal_Q

import time
import sys

#paper: Community structure in social and biological networks

class GN:
    
    def __init__(self, G):
        self._G_cloned = clone_graph(G)
        self._G = G
        self._partition = [[n for n in G.nodes()]]
        self._max_Q = 0.0
        
    def execute(self):
        while len(self._G.edges()) != 0:
            edge = max(nx.edge_betweenness(self._G).items(),key=lambda item:item[1])[0]
            self._G.remove_edge(edge[0], edge[1])
            components = [list(c) for c in list(nx.connected_components(self._G))]
            if len(components) != len(self._partition):
                cur_Q = cal_Q(components, self._G_cloned)
                if cur_Q > self._max_Q:
                    self._max_Q = cur_Q
                    self._partition = components
        #print(self._max_Q)
        #print(self._partition)
        return self._partition
        
    
if __name__ == '__main__':
    path_list = ['network/club.txt',
                 'data/facebook_combined.txt']
    graph_path = path_list[0]
    rate = 1.0
    if len(sys.argv) == 2:
        rate = float(sys.argv[1])
    G = load_graph_sample(graph_path, rate)

    start_time = time.time()
    algorithm = GN(G)
    communities = algorithm.execute()
    execution_time = (time.time() - start_time)
    time_length = '{0:.2f} s'.format(execution_time)
    Q = 0
    #print(cal_Q(communities, G))
    #print(len(communities))
    #print(time_length)
    #for community in communities:
    #    print(community)
    print("GN", time_length, rate, len(communities), algorithm._max_Q)


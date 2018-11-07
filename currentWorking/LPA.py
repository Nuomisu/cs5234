import collections
import random
import networkx as nx

from util.graph_helper import load_graph
from util.graph_helper import load_graph_sample
from util.graph_helper import clone_graph
from util.modularity import cal_Q

import time
import sys

'''
paper : <<Near linear time algorithm to detect community structures in large-scale networks>>
'''

class LPA():
    
    def __init__(self, G, max_iter = 20):
        self._G = G
        self._n = len(G.node) #number of nodes
        self._max_iter = max_iter
        
    def can_stop(self):
        # all node has the label same with its most neighbor
        for i in range(self._n):
            node = self._G.node[i]
            label = node["label"]
            max_labels = self.get_max_neighbor_label(i)
            if(label not in max_labels):
                return False
        return True
        
    def get_max_neighbor_label(self,node_index):
        m = collections.defaultdict(int)
        for neighbor_index in self._G.neighbors(node_index):
            neighbor_label = self._G.node[neighbor_index]["label"]
            m[neighbor_label] += 1
        max_v = max(m.values())
        return [item[0] for item in m.items() if item[1] == max_v]

    
    '''asynchronous update'''
    def populate_label(self):
        #random visit
        visitSequence = random.sample(self._G.nodes(),len(self._G.nodes()))
        for i in visitSequence:
            node = self._G.node[i]
            label = node["label"]
            max_labels = self.get_max_neighbor_label(i)
            if(label not in max_labels):
                newLabel = random.choice(max_labels)
                node["label"] = newLabel
        
    def get_communities(self):
        communities = collections.defaultdict(lambda:list())
        for node in self._G.nodes(True):
            label = node[1]["label"]
            communities[label].append(node[0])
        return communities.values()

    def execute(self):
        #initial label
        for i in range(self._n):
            self._G.node[i]["label"] = i
        iter_time = 0
        #populate label
        while(not self.can_stop() and iter_time<self._max_iter):
            self.populate_label()
            iter_time += 1
        return self.get_communities()
    
    
if __name__ == '__main__':
    path_list = ['network/club.txt',
                'data/facebook_combined.txt']
    graph_path = path_list[1]
    rate = 1.0
    if len(sys.argv) == 2:
        rate = float(sys.argv[1])
    G = load_graph_sample(graph_path, rate)

    start_time = time.time()
    # G = nx.karate_club_graph()
    algorithm = LPA(G)
    communities = algorithm.execute()

    execution_time = (time.time() - start_time)
    time_length = '{0:.2f} s'.format(execution_time)
    Q = 0
    #print(cal_Q(communities, G))
    #print(len(communities))
    #print(time_length)
    #for community in communities:
    #    print(community)
    print("LPA", time_length, rate, len(communities), Q)

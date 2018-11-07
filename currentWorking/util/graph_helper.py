import networkx as nx
from random import random

def load_graph_sample(path, rate):
    G = nx.Graph()
    mapping = dict()
    edges = []
    with open(path) as text:
        for line in text:
            r = random()
            if r > rate:
                continue
            vertices = line.strip().split(" ")
            source = int(vertices[0])
            target = int(vertices[1])
            edges.append((source, target))
            mapping[source] = 0
            mapping[target] = 0
    counter = 0
    for key in sorted(mapping):
        mapping[key] = counter
        counter += 1
    for edge in edges:
        G.add_edge(mapping[edge[0]], mapping[edge[1]])
    return G

def load_graph(path):
    G = nx.Graph()
    with open(path) as text:
        for line in text:
            vertices = line.strip().split(" ")
            source = int(vertices[0])
            target = int(vertices[1])
            G.add_edge(source, target)
    return G


def clone_graph(G):
    cloned_g = nx.Graph()
    for edge in G.edges():
        cloned_g.add_edge(edge[0], edge[1])
    return cloned_g

if __name__ == "__main__":
    G = load_graph('../network/club.txt')
    print(len(G.nodes(False)))
    print(len(G.edges(None, False)))

    g2 = clone_graph(G)
    print(g2.nodes())


#     for edge in G.edges(None, False):
#         print edge

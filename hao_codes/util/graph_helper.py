import networkx as nx
from random import random, randint, uniform, choice
from copy import deepcopy


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


def random_walk_sampling(path, rate, start_node=None, metropolized=False):
    G = load_graph(path)
    nmax = int(len(G.edges()) * rate)
    iteration = nmax
    sv = start_node

    if start_node is None:
        sv = choice(list(G.nodes()))

    G_sampled = nx.Graph()
    mapping = dict()
    edges = []

    v = sv
    print('Start node: {}'.format(v))
    while iteration > 0:
        # print('iteration: {}'.format(nmax - iteration + 1))
        iteration -= 1
        source = v
        # target = v
        if metropolized:
            candidate = choice(list(G.neighbors(v)))
            v = candidate if (random() < float(G.degree(v)) / G.degree(candidate)) else v
            target = v
        else:
            v = choice(list(G.neighbors(v)))
            target = v

        edges.append((source, target))
        mapping[source] = 0
        mapping[target] = 0

    counter = 0
    for key in sorted(mapping):
        mapping[key] = counter
        counter += 1

    for edge in edges:
        G_sampled.add_edge(mapping[edge[0]], mapping[edge[1]])

    return G_sampled
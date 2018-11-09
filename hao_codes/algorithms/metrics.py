import networkx as nx

def internal_density(community):
    '''

    :param G: (networkx.classes.graph.Graph): NetworkX graph
    :param communities: List of sets.
    :return: float
    '''
    # edges = G.edges(None, False)
    ms = len(community.edges())
    ns = len(community.nodes())
    try:
        internal_density = float(ms) / float(ns * (ns - 1)) / 2
    except:
        return 0
    return internal_density


def cut_ratio(G, community):
    '''

    :param G: (networkx.classes.graph.Graph): NetworkX graph
    :param communities: List of sets
    :return: float
    '''
    ns = len(community.nodes())
    edges_outside = 0
    for n in community.nodes():
        neighbors = G.neighbors(n)
        for n1 in neighbors:
            if n1 not in community:
                edges_outside += 1
    try:
        ratio = float(edges_outside) / (ns * (len(G.nodes()) - ns))
    except:
        return 0
    return ratio

def expansion(G, community):
    ns = len(community.nodes())
    edges_outside = 0
    for n in community.nodes():
        neighbors = G.neighbors(n)
        for n1 in neighbors:
            if n1 not in community:
                edges_outside += 1
    try:
        return float(edges_outside) / ns
    except:
        return 0



def conductance(G, community):
    '''

    :param G: (networkx.classes.graph.Graph): NetworkX graph
    :param communities: List of nodes
    :return: float
    '''
    ms = len(community.edges())
    edges_outside = 0
    for n in community.nodes():
        neighbors = G.neighbors(n)
        for n1 in neighbors:
            if n1 not in community:
                edges_outside += 1
    try:
        ratio = float(edges_outside) / ((2 * ms) + edges_outside)
    except:
        return 0
    return ratio


def modularity(G, communities):
    '''

    :param G: (networkx.classes.graph.Graph): NetworkX graph
    :param communities: List of sets.
    :return: float
    '''
    m = len(G.edges())
    a = []
    e = []

    for community in communities:
        t = 0.0
        for node in community:
            t += len(list(G.neighbors(node)))
        a.append(t / (2 * m))

    for community in communities:
        t = 0.0
        for i in range(len(community)):
            for j in range(len(community)):
                if (G.has_edge(community[i], community[j])):
                    t += 1.0
        e.append(t / (2 * m))

    q = 0.0
    for ei, ai in zip(e, a):
        q += (ei - ai ** 2)

    return q

def community_modularity(coms, g):
    if type(g) != nx.Graph:
        raise TypeError("Bad graph type, use only non directed graph")

    inc = dict([])
    deg = dict([])
    links = g.size(weight='weight')
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")

    for node in g:
        try:
            com = coms[node]
            deg[com] = deg.get(com, 0.) + g.degree(node, weight='weight')
            for neighbor, dt in g[node].items():
                weight = dt.get("weight", 1)
                if coms[neighbor] == com:
                    if neighbor == node:
                        inc[com] = inc.get(com, 0.) + float(weight)
                    else:
                        inc[com] = inc.get(com, 0.) + float(weight) / 2.
        except:
            pass

    res = 0.
    for com in set(coms.values()):
        res += (inc.get(com, 0.) / links) - (deg.get(com, 0.) / (2.*links))**2
    return res

def modularity_gai(g, coms):
    part = {}
    ids = 0
    for c in coms:
        for n in c:
            part[n] = ids
        ids += 1

    mod = community_modularity(part, g)
    return mod
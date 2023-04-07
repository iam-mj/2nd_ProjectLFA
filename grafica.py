import matplotlib.pyplot as plt
import networkx as nx
from netgraph import Graph


def desen(QL, D, qi, F):
    #ne stocam muchiile intr-un dictionar
    D1 = {}

    for lista in D:
        if lista[0] not in D1:
            D1[lista[0]] = {lista[1] : [lista[2]]}
        elif lista[1] not in D1[lista[0]]:
            D1[lista[0]][lista[1]] = [lista[2]]
        else:
            D1[lista[0]][lista[1]].append[lista[2]]

    G = nx.DiGraph()
    for start in D1:
        for final in D1[start]:
            G.add_edge(start, final, label = ', '.join([x if x != ' ' else '\' \'' for x in D1[start][final]]))
    edge_labels = nx.get_edge_attributes(G, 'label')

    pos = nx.planar_layout(G)
    
    #adaugam culori pt a identifica nodurile speciale
    colors = {}
    for nod in QL:
        if nod in F:
            colors[nod] = '#337bb8'
        elif nod == qi:
            colors[nod] = '#9fc5e5'
        else:
            colors[nod] = '#63a0d4'
    
    Graph(G, node_layout = pos, edge_layout = 'curved', origin = (-1, -1), scale = (2, 2),
        node_color = colors, node_size = 8, node_labels = True, node_label_fontdict = dict(size = 10),
        edge_labels = edge_labels, edge_label_fontdict = dict(size = 10), edge_label_position = 0.7, arrows = True
    )
    plt.show()
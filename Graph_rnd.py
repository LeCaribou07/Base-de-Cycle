from numba import jit, cuda
import matplotlib.pyplot as plt

import networkx as nx

import sys
import os
import time


'''
Fonction permettant de créer un graphe de type Graph() de la libraire networkx à partir d'un fichier .rnd
'''
def create_graph_from_rnd_file(rnd):
    nxgraph = nx.Graph()
    i = 0
    with open(rnd, "r") as file:
        for line in file:
            if i == 1:
                i += 1
                y = line.split()
                for j in range(1, int(y[0])+1):
                    nxgraph.add_node(str(j))
            elif i > 1:
                i += 1
                y = line.split()
                nxgraph.add_edge(str(y[0]), str(y[1]))
            else:
                i += 1
    return nxgraph

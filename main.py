import os
import sys
import time

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from Graph_rnd import *
from gf_2_test import fast_Horton_over_GF2

'''
Fonction permettant de construire une base de l'espace des cycles à l'aide d'un théorème de la théorie algébrique
des graphes
'''
def construct_basis(graph):

    basis = []

    a = nx.minimum_spanning_tree(graph)

    a_temp = a.copy()
    edges_of_tree = a.edges()
    edges_of_diff = graph.copy()
    edges_of_diff.remove_edges_from(edges_of_tree)
    edges_of_diff = edges_of_diff.edges()

    for w in edges_of_diff:
        a_temp.add_edge(w[0], w[1])
        cycle = list(nx.find_cycle(a_temp))
        basis.append(cycle)
        a_temp = a.copy()

    return basis


'''
Fonction permettant de réaliser des benchmark sur l'algorithme de De Pina présent dans networkx
'''
def Bench_DePina(_path):
    i = 1
    final_time = 0
    rndFile = os.listdir(_path)
    for file in rndFile:
        nxgraph = create_graph_from_rnd_file(_path + '/' + file)
        start_time_basis = time.time()
        b = nx.cycle_basis(nxgraph)
        final_time += time.time() - start_time_basis
        i += 1
    return final_time


'''
Afiche quelques propriétés des graphes : rayon, diamètre et densité
'''
def func_properties(_path):
    print("name,radius,diameter,density\n")
    rndFile = os.listdir(_path)
    print("debut")
    for file in rndFile:
        nxgraph = create_graph_from_rnd_file(_path + '/' + file)
        r, diam, d = property(nxgraph)
        string = f'{file},{r},{diam},{d}'
        print(string)


def max_of_list(list):
    max = 0
    for element in list:
        if len(element) > max:
            max = len(element)
    return max


def result(graph):
    start = time.time()
    B = nx.minimum_cycle_basis(graph)
    basis_dimension = graph.number_of_edges() - graph.number_of_nodes() + 1
    print(f'{time.time() - start}, {len(B)} = {basis_dimension}, taille du plus cycle : {max_of_list(B)}')
    

if __name__ == '__main__':

    g = create_graph_from_rnd_file("Harwell-Boeing BRP Instances\\bcspwr02.mtx.rnd")
    basis = fast_Horton_over_GF2(g)
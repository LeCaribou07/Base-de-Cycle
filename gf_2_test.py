import numpy as np 
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import sympy
import scipy.linalg as la
import numpy as np
import sys
import os
import time


'''
Calcul le rang d'une matrice binaire sur le corps GF(2)
'''
def gf2_rank(rows):
    """
    Find rank of a matrix over GF2.

    The rows of the matrix are given as nonnegative integers, thought
    of as bit-strings.

    This function modifies the input list. Use gf2_rank(rows.copy())
    instead of gf2_rank(rows) to avoid modifying rows.
    """
    rank = 0
    while rows:
        pivot_row = rows.pop()
        if pivot_row:
            rank += 1
            lsb = pivot_row & -pivot_row
            for index, row in enumerate(rows):
                if row & lsb:
                    rows[index] = row ^ pivot_row
    return rank


def bool_matrice_to_bin_list(matrice):
    L = []
    for list in matrice:
        L.append(int("".join(str(x) for x in list), 2))
    return L


def reverse_tuple(tuple):
    new_tuple = tuple[::-1]
    return new_tuple


'''
Fonction calculant le vecteur associé à un cycle C pour un graphe G.
'''

def mu(graphe, cycle):
    v = []
    for e in graphe.edges():
        if e in cycle or reverse_tuple(e) in cycle:
            v.append(1)
        else:
            v.append(0)
    return v


'''
Autre méthode pour le calcul le rang d'une matrice binaire sur le corps GF(2)

'''
def binary_rank(M) :
    
    # M-pty matrix?
    if not np.count_nonzero(M): return 0

    # Find any nonzero entry, i.e. the pivot
    (p, q) = tuple(a[0] for a in np.nonzero(M))

    # Indices of entries to flip
    # (Could filter out p and q)
    I = np.nonzero(M[:, q])[0]
    J = np.nonzero(M[p, :])[1]

    # Flip those entries
    for i in I :
        for j in J :
            M[i, j] = not M[i, j]

    # Zero out pivot row p / column q
    # (Or delete them from the matrix)
    M[p, :] = 0
    M[:, q] = 0
    
    return 1 + binary_rank(M)



def fast_Horton_over_GF2(graph):
    # Plus court chemin entre chaques sommets
    # Le graphe étant non-orienté, on a P(x, y) = P(y, x)
    basis = []
    cycle = []
    for v in graph.nodes():
        T = nx.bfs_tree(graph, v)
        for x, y in graph.edges():
            path_v_to_x = nx.shortest_path(T, source=v, target=x)
            path_v_to_y = nx.shortest_path(T, source=v, target=y)
            c = []
            if set(path_v_to_x) & set(path_v_to_y) == {v}:
                for i in range(len(path_v_to_x)-1):
                    c.append((path_v_to_x[i], path_v_to_x[i+1]))
                for i in range(len(path_v_to_y)-1):
                    c.append((path_v_to_y[i], path_v_to_y[i+1]))
                c.append((x, y))
                g = nx.Graph()
                g.add_edges_from(c)
                try:
                    cy = nx.find_cycle(g)
                    cycle.append(cy)
                except:
                    pass
    cycle.sort(key=len)

    basis.append(cycle[0])
    cycle = cycle[1:]
    t = []
    for element in basis:
        t.append(mu(graph, element))

    nu = graph.number_of_edges() - graph.number_of_nodes() + 1
    while len(basis) < nu:
        c = cycle[0]
        mu_c = mu(graph, c)
        t.append(mu_c)
        l = len(basis)
        p = bool_matrice_to_bin_list(t)
        if gf2_rank(p) == l + 1:
            basis.append(c)
        else:
            t = t[:-1]
        cycle = cycle[1:]
    return basis
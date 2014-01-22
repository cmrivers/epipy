#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
 CASE TREE PLOT
 -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
 -------------
 Case trees are a type of plot I've developed^ to visualize clusters
 of related cases in an outbreak. They are particularly useful for
 visualizing zoonoses.

 My wish list for improvements includes:
 * add an option to include nodes that have no children, i.e. are not
   part of a human to human cluster
 * create a legend to label which colors correspond to which node
   attributes
 * improve color choice reliabely produces an attractive color palette

 ^ I have seen similar examples in the literature,
   e.g. Antia et al (Nature 2003)
"""

from __future__ import division
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from random import choice
from matplotlib import cm

def build_graph(df, case_id='case_id', color='color', index='index_node',
		source='source_node', date='pltdate'):
    """
    Generate a directed graph from data on transmission tree.
    Node color is determined by node attributes, e.g. case severity or gender.
    df = pandas dataframe """
    G = nx.DiGraph()
    G.add_nodes_from(df[case_id])

    edgelist = [pair for pair in df[[source]].dropna().itertuples()]
    G.add_edges_from(edgelist)
    nx.set_node_attributes(G, date, df[date].to_dict())
    nx.set_node_attributes(G, source, df[source].to_dict())
    nx.set_node_attributes(G, color, df[color].to_dict())
    nx.set_node_attributes(G, index, df[index].to_dict())
    G = nx.DiGraph.reverse(G)

    return G


def case_tree_plot(G, node_size=100):
    """
    Plot casetree
    G = networkx object
    node_size = on (display node) or off (display edge only). Default is on.
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.xaxis_date()
    ax.set_aspect('auto')
    axprop =  ax.axis()

    coords = _layout(G)
    plt.ylim(ymin=-.05, ymax=max([val[1] for val in coords.itervalues()])+1)


    colormap, color_floats = _colors(G, 'color')
    print colormap

    x_val = G.nodes()[0]
    lines = []

    for key, value in colormap.iteritems():
        plt.scatter(G.node[x_val]['pltdate'], value[0], color=value, alpha=0)
        line = plt.Line2D(range(1), range(1), color=value, marker='o', markersize=10, alpha=.6, label=key)
        lines.append(line)

    ax.legend(lines, [k for k in colormap.iterkeys()])

    nx.draw_networkx(G, ax=ax, with_labels=False, pos=coords, node_color=color_floats,
                     node_size=node_size, alpha=.6)

    fig.autofmt_xdate()

    return fig, ax


def _colors(G, color):
    """
    Determines colors of the node based on node attribute,
	e.g. case severity or gender.
    G = networkx object
    color = name of node attribute in graph used to assign color
    """
    # collect list of unique attributes from graph
    categories = []
    for node in G.nodes():
        categories.append(G.node[node][color])

    # create color map of attributes and colors
    colors = cm.Accent(np.linspace(0, 1, len(categories)))
    colordict = dict(zip(categories, colors))

    color_floats = []
    for node in G.nodes():
        G.node[node]['plot_color'] = colordict[G.node[node][color]]
        color_floats.append(colordict[G.node[node][color]])


    return colordict, color_floats


def _generations(G, node):
    """ Recursively determines the generation of the node, e.g. how many
    links up the chain of transmission it is.
    This value is used as the y coordinate.
    G = networkx object
    node = node in network
    """
    levels = 0

    while node != G.node[node]['source_node']:
        node = G.node[node]['source_node']
        levels += 1

    return levels


def _layout(G):
    """Determine x and y coordinates of each node.
    G = networkx object
    axprop = matplotlib axis object
    """
    np.random.seed(0)  # consistent layout between runs(?)
    positions = []

    for i in G.nodes():
        # index node (generation = 0)
        if i == G.node[i]['index_node']:
            xcord = G.node[i]['pltdate']
            generation = 0.1

        # children (generation > 0)
        else:
            # if the coordinates exist, jitter the y coord to make space
            ix = G.node[i]['source_node']
            generation = _generations(G, i)
            ix = i
            xcord = G.node[ix]['pltdate']

            jittery = np.random.uniform(-.2, .2, 1)
            generation = generation + jittery

        G.node[i]['xcord'] = xcord
        G.node[i]['generation'] = generation
        positions.append([xcord, generation])

    return dict(zip(G, np.array(positions)))

import epipy
import pandas as pd
test_df = pd.read_pickle('../data/test_cluster.pkl')
test_clusters = epipy.cluster_builder(test_df, 'Cluster', 'ID', 'Date', 'Cluster', 5, 1)
test_G = epipy.build_graph(test_clusters)
fig, ax = case_tree_plot(test_G, node_size=100)
fig.show()
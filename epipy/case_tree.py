#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import basics
import matplotlib.pyplot as plt
import networkx as nx

def build_graph(df, cluster_id, case_id, date_col, color, gen_mean, gen_sd, palette=None):
    """
    Generate a directed graph from data on transmission tree.
    Node color is determined by node attributes, e.g. case severity or gender.
    df = pandas dataframe
    """

    clusters = basics.cluster_builder(df=df, cluster_id=cluster_id, \
                case_id=case_id, date_col=date_col, attr_col=color, \
                gen_mean=gen_mean, gen_sd=gen_sd)

    G = nx.DiGraph()
    G.add_nodes_from(clusters['case_id'])

    edgelist = [pair for pair in clusters[['source_node']].dropna().itertuples()]
    G.add_edges_from(edgelist)
    nx.set_node_attributes(G, 'date', clusters['time'].to_dict())
    nx.set_node_attributes(G, 'pltdate', clusters['pltdate'].to_dict())
    nx.set_node_attributes(G, 'source_node', clusters['source_node'].to_dict())
    nx.set_node_attributes(G, color, clusters[color].to_dict())
    nx.set_node_attributes(G, 'index_node', clusters['index_node'].to_dict())
    G = nx.DiGraph.reverse(G)

    for i in G.nodes():
        G.node[i]['generation'] = _generations(G, i)

    return G



def plot_tree(G, color, node_size, loc, legend, color_palette, fig, ax):

    if ax is None or fig is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    fig.autofmt_xdate()
    ax.xaxis_date()
    ax.set_aspect('auto')

    coords = _layout(G)
    plt.ylim(ymin=-.05, ymax=max([val[1] for val in coords.itervalues()])+1)

    colormap, color_floats = _colors(G, color, color_palette=color_palette)

    if legend == True:
        x_val = G.nodes()[0]
        lines = []

        for key, value in colormap.iteritems():
            plt.scatter(G.node[x_val]['pltdate'], value[0], color=value, alpha=0)
            line = plt.Line2D(range(1), range(1), color=value, marker='o', markersize=6, alpha=.8, label=key)
            lines.append(line)

        ax.legend(lines, [k for k in colormap.iterkeys()], loc=loc)

    nx.draw_networkx(G, ax=ax, with_labels=False, pos=coords, node_color=color_floats,
                     node_size=node_size, alpha=.8)

    return fig, ax


def case_tree_plot(df, cluster_id, case_id, date_col, color, \
                    gen_mean, gen_sd, node_size=100, loc='best',\
                    legend=True, color_palette=None, fig=None, ax=None):
    """
    Plot casetree
    df = pandas dataframe, line listing
    cluster_id = col that identifies cluster membership. Can be a
        basic string like "hospital cluster A"
    case_id = col with unique case identifier
    date_col = onset or report date column
    color = column that will be used to color nodes based on
        attribute, e.g. case severity or gender
    gen_mean = generation time mean
    gen_sd = generation time standard deviation
    node_size = on (display node) or off (display edge only). Default is on.
    loc = legend location. See matplotlib args.
    legend = True for legend, False for no legend
    color_palette = dictionary of category:color pairs OR a list of colors
    fig, ax = fig ax objects
    """
    G = build_graph(df, cluster_id, case_id, date_col, color, \
                      gen_mean, gen_sd)

    fig, ax = plot_tree(G, color, node_size, loc, legend, color_palette, fig, ax)

    return G, fig, ax


def _colors(G, color, color_palette=None):
    """
    Determines colors of the node based on node attribute,
	e.g. case severity or gender.
    G = networkx object
    color = name of node attribute in graph used to assign color
    """
    # collect list of unique attributes from graph
    if type(color_palette) != dict:
        categories = []
        for node in G.nodes():
            categories.append(G.node[node][color])

        categories = np.unique(categories)
        # create color map of attributes and colors
        if type(color_palette) == list:
            colors = color_palette
        else:
            colors = [color for i, c in enumerate(plt.rcParams['axes.color_cycle'])]
            
        color_dict = dict(zip(categories, colors))
        
    elif type(color_palette) == dict:
        color_dict = color_palette        

    color_floats = []
    for node in G.nodes():
        G.node[node]['plot_color'] = color_dict[G.node[node][color]]
        color_floats.append(color_dict[G.node[node][color]])


    return color_dict, color_floats


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
        xcord = G.node[i]['pltdate']
        generation = G.node[i]['generation']
        if generation == 0:
            ygen = generation
        else:
            jittery = np.random.uniform(-.2, .2, 1)
            ygen = generation + jittery

        positions.append([xcord, ygen])

    return dict(zip(G, np.array(positions)))



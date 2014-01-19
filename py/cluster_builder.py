# -*- coding: utf-8 -*-
# # Basic transmission tree builder
# 
# * Caitlin Rivers
# 
# * Virginia Bioinformatics Institute at Virginia Tech
# 
# * cmrivers@vbi.vt.edu
# 
# -------
#
# Given a line listing with dates and basic information about cluster
# membership, this script will estimate who transmitted an infectious
# disease to whom based on case onset dates.
# 
# Wish list for improvements:
# 
# * Make algorithm that determines who infected whom more sophisticated.
# 
# * Find a way to keep single cases (e.g. those not part of a cluster)
#   in the data set so they can be plotted on the casetree.


from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
from itertools import cycle
try:
    from mpltools import style, layout
    style.use('ggplot')
except:
    pass


def date_convert(x):
    """ Convert dates to datetime object
    """
    try:
        y = datetime.strptime(x, "%Y-%m-%d")
    except:
        y = np.nan
        
    return y


def _group_clusters(df, cluster_id, date_col):
    ''' Use pandas to group clusters by basic cluster membership information
    df = pandas dataframe
    cluster_id = column that identifies cluster membership, which can
	be a basic string like "hospital cluster A"
    date_col = onset or report date column
    '''
    clusters = df[df[cluster_id] != 'single']
    clusters = clusters[clusters[date_col].notnull()]
    
    groups = clusters.groupby(clusters[cluster_id])
    
    return groups


def cluster_builder(df, cluster_id, case_id, date_col, color_col, gen_mean, gen_sd):
    '''
    Given a line listing with dates and basic info about cluster membership,
    this script will estimate who transmitted an infectious disease to
    whom based on case onset dates.

    df = pandas dataframe of line listing
    cluster_id = col that identifies cluster membership, which can be a
	basic string like "hospital cluster A"
    case_id = col with unique case identifier
    date_col = onset or report date column
    color_col = column that will be used to color nodes based on
	attribute, e.g. case severity or gender
    gen_mean = generation time mean
    gen_sd = generation time standard deviation

    returns networkx object
    '''
    clusters = _group_clusters(df, cluster_id, date_col)
    
    gen_min = timedelta((gen_mean - gen_sd), 0)
    gen_max = timedelta((gen_mean + gen_sd), 0)
    
    cluster_obj = []
    for key, group in clusters:
        if len(group) > 1:
            row = [tmp[1:4] for tmp in group[[case_id, date_col, color_col]].sort(date_col, ).itertuples()]
            cluster_obj.append(row)

    global cluster_obj
    network = []
    for cluster in cluster_obj:
	cluster = np.array(cluster[::-1]) #reverse dates, last case first
	ids = cluster[:, 0]
	dates = cluster[:, 1]
	colors = cluster[:, 2]

        index_node = ids[-1]
        source_nodes = []
        for i, (date, idx) in enumerate(zip(dates, ids)):
            start_date = date - gen_max
            start_node = ids[dates >= start_date][-1]

	    if start_node == idx and idx != index_node:
                start_node = ids[i+1]
	    
            source_nodes.append(start_node)

        for i in range(len(ids)):
	    result = (ids[i], colors[i], index_node, source_nodes[i], dates[i])
            network.append(result)
            
    df_out = pd.DataFrame(network, columns=['case_id', 'color', 'index_node', 'source_node', 'time'])
    df_out.index = df_out.case_id
    
    return df_out


def plot_cluster(df, case_id, clusters, cluster_id, date_col):
    '''
    '''
    clusters = _group_clusters(dat, cluster_id, date_col)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.xaxis_date()
    ax.set_aspect('auto')
    axprop =  ax.axis()
    
    grpnames = [key for key, group in clusters if len(group) > 1]
    plt.ylim(1, len(grpnames))
    plt.yticks(np.arange(len(grpnames)), grpnames)
    
    xtog = timedelta(((10*axprop[1]-axprop[0])/axprop[1]), 0, 0)
    counter = 0
    cols = cycle([color for i, color in enumerate(plt.rcParams['axes.color_cycle'])])
    
    for key, group in clusters:
        if len(group) > 1:
            color = next(cols)
            casenums = cycle([int(num) for num in group.index])
            
            positions = []
            for casedate in group[date_col].order():
                x1 = casedate
                x2 = casedate + xtog
                positions.append(x2)
                
                y1 = np.array([counter, counter])
                y2 = y1 + 1
                
                plt.fill_between([x1, x2], y1, y2, color=color, alpha=.3)
                yposition = y1[0] + .5
                
                try:
                    if x1 <= positions[-2]:
                        yposition = yposition + np.random.uniform(-.4, .4, 1)
                except:
                    pass
                    
                textspot= x1 + timedelta((x2 - x1).days/2.0, 0, 0)
                plt.text(textspot, yposition, next(casenums), horizontalalignment='center', 
                         verticalalignment='center', fontsize=9)    
                
            counter += 1
            
    fig.autofmt_xdate()
    fig.tight_layout()
    
    return fig, ax


# Data (from 2013 MERS outbreak) are available in cmrivers/epipy repo on Github.

dat = pd.read_csv("../data/Line list & epi stats - Line list.csv", parse_dates=True)

dat['Cluster ID'] = dat['Cluster ID'].replace(np.nan, 'single')
dat.index = dat['Case #']
dat['onset_date'] = dat['Approx onset date'].map(date_convert)
dat['report_date'] = dat['Approx reporting date'].map(date_convert)
dat['dates'] = dat['onset_date'].combine_first(dat['report_date']) #combines onset and report date columns, with onset date preferential

clusters = cluster_builder(dat, 'Cluster ID', 'Case #', 'dates', 'Cluster ID', 8, 4)
clusters.to_pickle('../data/cluster_network.pkl')

fig, ax = plot_cluster(dat, clusters, 'Case #', 'Cluster ID', 'dates')
ax.set_title("MERS-CoV clusters")
fig.savefig('../figs/cluster_checkerboard.png')

#dat = pd.read_pickle('test_cluster.pkl')
#dat.index=dat['ID']
#clusters = cluster_builder(dat, 'Cluster', 'ID', 'Date', 'Cluster', 5, 1)
#clusters.to_pickle('../data/test_cluster.pkl')

#fig, ax = plot_cluster(dat, clusters, 'ID', 'Cluster', 'Date')
#ax.set_title("test clusters")
#fig.savefig('../figs/test_clusters.png')



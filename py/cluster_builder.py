# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

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
# Given a line listing with dates and basic information about cluster membership, this script will estimate who transmitted an infectious disease to whom based on case onset dates.
# 
# Wish list for improvements:
# 
# * Make algorithm that determines who infected whom more sophisticated.
# 
# * Find a way to keep single cases (e.g. those not part of a cluster) in the data set so they can be plotted on the casetree.
# 
# * Fix plot_cluster() function so it is functional.

# <codecell>

from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

# <codecell>

def date_convert(x):
    """ Convert dates to datetime object
    """
    try:
        y = datetime.strptime(x, "%Y-%m-%d")
    except:
        y = np.nan
        
    return y

# <markdowncell>

# Data (from 2013 MERS outbreak) are available in cmrivers/epipy repo on Github.

# <codecell>

dat = pd.read_csv("./Line list & epi stats - Line list.csv", parse_dates=True)
dat['Cluster ID'] = dat['Cluster ID'].replace(np.nan, 'single')
dat.index = dat['Cluster ID']

# <codecell>

dat['onset_date'] = dat['Approx onset date'].map(date_convert)
dat['report_date'] = dat['Approx reporting date'].map(date_convert)
dat['dates'] = dat['onset_date'].combine_first(dat['report_date']) #combines onset and report date columns, with onset date preferential

# <codecell>

def _group_clusters(df, cluster_id, date_col):
    ''' Use pandas to group clusters by basic cluster membership information
    df = pandas dataframe
    cluster_id = column that identifies cluster membership, which can be a basic string like "hospital cluster A"
    date_col = onset or report date column
    '''
    clusters = df[df[cluster_id] != 'single']
    clusters = clusters[clusters[date_col].notnull()]
    
    groups = clusters.groupby(clusters[cluster_id])
    
    return groups

# <codecell>

def cluster_builder(df, cluster_id, case_id, date_col, color_col, inc_mean, inc_sd):
    '''
    Given a line listing with dates and basic information about cluster membership,
    this script will estimate who transmitted an infectious disease to whom based on case onset dates.

    df = pandas dataframe of line listing
    cluster_id = col that identifies cluster membership, which can be a basic string like "hospital cluster A"
    case_id = col with unique case identifier
    date_col = onset or report date column
    color_col = column that will be used to color nodes based on attribute, e.g. case severity or gender
    inc_mean = incubation period mean
    inc_sd = incubation period standard deviation

    retuns clusters (pandas dataframe) and mx (network x object)
    '''
    clusters = _group_clusters(df, cluster_id, date_col)
    
    mmin = timedelta(inc_mean - (1 * inc_sd), 0)
    mmax = timedelta(inc_mean + (1 * inc_sd), 0)
    
    mx = []
    for key, group in clusters:
        row = [tmp[1:4] for tmp in group[[case_id, date_col, color_col]].sort('dates').itertuples()] #suspect this will be buggy with dif data sets, woudl like to improve
        mx.append(row)

    network = []
    for ix in range(0, len(mx)):
        for inx in range(0, len(mx[ix])):
            index_node = mx[ix][0][0]
            source_node = index_node
            case_id = mx[ix][inx][0]
            time = mx[ix][inx][1]
            color = mx[ix][inx][2]
            
            if len(mx[ix]) > 1:
               if mx[ix][inx][1] - mx[ix][inx-1][1] > mmin:
                    source_node = mx[ix][inx-1][0]
        
            result = (case_id, color, index_node, source_node, time)
            network.append(result)
            
    df_out = pd.DataFrame(network, columns=['case_id', 'color', 'index_node', 'source_node', 'time'])
    df_out.index = df_out.case_id
    
    return clusters, mx

# <codecell>

clusters, mx = cluster_builder(dat, 'Cluster ID', 'Case #', 'dates', 'Health status', 7, 5)

# <codecell>

mx.save('./cluster_network.pkl')

# <codecell>

def plot_cluster(df, cluster_id, date_col):
    """Broken. Date-handling patience gone.

    Should display a plot with time along x axis, cluster ID along y axis,
    and case ID plotted like a scatterplot accordingly.
    """
    grpnames = np.unique(df[cluster_id]).dropna().values
    
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 5)
    ax.xaxis_date()
    ax.set_aspect('auto')
    axprop =  plt.axis()
    fig.autofmt_xdate()
    
    plt.ylim(1, len(grpnames))
    plt.yticks(np.arange(len(grpnames)), grpnames)
    
    for key, group in clusters:
        for date in date_col:
            xtog = timedelta(((10*axprop[1]-axprop[0])/axprop[1]), 0, 0)
            x1 = [date, date+xtog]
    
            for i in range(len(grpnames)):
                if key == grpnames[i]:
                    y1 = np.array([i, i])
                    y2 = y1+0.5
                    plt.fill_between(x1, y1, y2, color=color, alpha=.3)
                    
                    xspot= x1[0] + timedelta((x1[1] - x1[0]).days/2.0, 0, 0)
                    
                    plt.text(xspot, y1[1]+.25, next(casenums), horizontalalignment='center', verticalalignment='center', fontsize=9)
                    
    return fig

# <codecell>

plot_cluster(dat, 'Cluster ID', 'dates')

# <codecell>



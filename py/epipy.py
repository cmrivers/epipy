#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
'''

import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def date_convert(date, str_format):
    """ Convert dates to datetime object
    """
    try:
        y = datetime.strptime(date, str_format)
    except:
        y = np.nan
        
    return y


def group_clusters(df, cluster_id, date_col):
    ''' Use pandas to group clusters by cluster identifier
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
    Given a line list with dates and info about cluster membership,
    this script will estimate the transmission tree of an infectious
    disease based on case onset dates.

    df = pandas dataframe of line list
    cluster_id = col that identifies cluster membership. Can be a
        basic string like "hospital cluster A"
    case_id = col with unique case identifier
    date_col = onset or report date column
    color_col = column that will be used to color nodes based on
        attribute, e.g. case severity or gender
    gen_mean = generation time mean
    gen_sd = generation time standard deviation

    returns pandas groupby dataframe 
    '''
    clusters = group_clusters(df, cluster_id, date_col)
    
    gen_max = timedelta((gen_mean + gen_sd), 0)
    
    cluster_obj = []
    for key, group in clusters:
        if len(group) > 1:
            row = [tmp[1:4] for tmp in group[[case_id, date_col, color_col]].sort(date_col, ).itertuples()]
            cluster_obj.append(row)

    network = []
    for cluster in cluster_obj:
        #reverse dates, last case first
        cluster = np.array(cluster[::-1]) 
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

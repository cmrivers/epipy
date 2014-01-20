# -*- coding: utf-8 -*-
'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
 I developed checkerboard plots as a companion to case tree plots. A
 checkerboard plot shows when cases in a cluster occurred or were
 diagnosed, without assuming how they are related.
'''
import epipy
import matplotlib.pyplot as plt
from datetime import timedelta
from itertools import cycle
import numpy as np

def plot_cluster(df, case_id, cluster_id, date_col):
    '''
    df = pandas dataframe
    case_id = unique identifier of the cases
    cluster_id = identifier for each cluster, e.g. FamilyA
    date_col = column of onset or report dates
    returns matplotlib figure and axis objects
    '''
    clusters = epipy.group_clusters(df, cluster_id, date_col)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.xaxis_date()
    ax.set_aspect('auto')
    axprop = ax.axis()
    
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
                ypos = y1[0] + .5
                
                try:
                    if x1 <= positions[-2]:
                        ypos = ypos + np.random.uniform(-.4, .4, 1)
                except:
                    pass
                    
                textspot = x1 + timedelta((x2 - x1).days/2.0, 0, 0)
                plt.text(textspot, ypos, next(casenums),
			    horizontalalignment='center', 
			    verticalalignment='center', fontsize=9)    
                
            counter += 1
            
    fig.autofmt_xdate()
    fig.tight_layout()
    
    return fig, ax

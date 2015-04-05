# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:02:11 2015

@author: caitlin
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

cases = pd.read_csv("cases.csv", parse_dates=['onset', 'death', 'discharged'], infer_datetime_format=True)
cases = cases.replace('nan', np.nan)
cases['combined_outcome'] = cases['death'].combine_first(cases['discharged'])
cases = cases[['number', 'onset', 'combined_outcome', 'outcome']].dropna(how='any').head(15)

# %%
def time_plot(df, yticks, date1, date2, color, color_dict=None, legend=True):
    
    fig, ax = plt.subplots()
    ax.xaxis_date()
    ax.set_aspect('auto')
    fig.autofmt_xdate()
    
    plt.ylim(-1, len(df))
    plt.yticks(np.arange(len(df)), df[yticks].values)
    
    color_keys = df[color].values
    if color_dict == None:
        color_choices = sns.color_palette('deep', len(color_keys))
    color_dict = dict(zip(color_keys, color_choices))
    
    counter = 0
    
    for ix in df[date1].order(ascending=False).index:
        x1 = df.xs(ix)[date1]
        x2 = df.xs(ix)[date2]
        
        y1 = counter
        
        col = color_dict[df.xs(ix)[color]]
        
        ax.scatter(x1, y1, color=col)
        ax.scatter(x2, y1, color=col)
        plt.fill_between([x1, x2], y1-.04, y1+.04, alpha=.8, color=col)

        counter += 1
        
            
    if legend == True:
        lines = []

        for key, value in color_dict.iteritems():
            plt.scatter(df[date1][0], value[0], color=value, alpha=0)
            line = plt.Line2D(range(1), range(1), color=value, marker='o', markersize=6, alpha=.8, label=key)
            lines.append(line)

        ax.legend(lines, [k for k in color_dict.iterkeys()])

    return fig, ax

fig, ax = time_plot(cases, 'number', 'onset', 'combined_outcome', 'outcome')
ax.set_title('Case histories of MERS patients')
ax.set_xlabel('Dates of onset, outcome')
ax.set_ylabel('Case number')

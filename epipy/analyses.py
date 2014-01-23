#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def reproduction_number(G, index_cases=True, summary=True, plot=True):
    """ 
    Finds each case's basic reproduction number, which is the number of secondary
    infections each case produces.
    
    PARAMETERS
    ----------------
    G = networkx object
    index_cases = include index nodes, i.e. those at generation 0. Default is True.
                  Excluding them is useful if you want to calculate the human to human
                  reproduction number without considering zoonotically acquired cases.
    summary = print summary statistics of the case reproduction numbers 
    plot = create histogram of case reproduction number distribution.
    
    RETURNS
    ----------------
    pandas series of case reproduction numbers and matplotlib figure
    and axis objects if plot=True
    """
    R = pd.Series(G.out_degree())

    if index_cases == False:
        R = R[R > 0]
    
    if summary == True:
        print 'Summary of reproduction numbers'
        print R.describe(), '\n'
        
    if plot == True:
        fig, ax = plt.subplots()
        R.hist(ax=ax, alpha=.5)
        ax.set_xlabel('Secondary cases')
        ax.set_ylabel('Count')
        ax.grid(False)
        return fig, ax, R

    else:
        return R


def generation_analysis(G, attribute, table=True, plot=True):
    """ 
    Analyzes an attribute, e.g. health status, by generation.
    
    PARAMETERS
    -------------
    G = networkx object
    attribute = case attribute for analysis, e.g. health status or sex
    table = print cross table of attribute by generation. Default is true.
    plot = produce histogram of attribute by generation. Default is true.
    
    RETURNS
    --------------
    matplotlib figure and axis objects
    
    """
    
    gen_df = pd.DataFrame(G.node).T
    
    if table == True:
        print '{} by generation'.format(attribute)
        table = pd.crosstab(gen_df.generation, gen_df[attribute], margins=True)
        print table, '\n'
    
    if plot == True:
        fig, ax = plt.subplots()
        ax.set_aspect('auto')
        pd.crosstab(gen_df.generation, gen_df[attribute]).plot(kind='bar', ax=ax, alpha=.5)
        ax.set_xlabel('Generation')
        ax.set_ylabel('Case count')
        ax.grid(False)
        ax.legend(loc='best');
        
    return fig, ax

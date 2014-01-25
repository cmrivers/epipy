#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
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

def two_x_two(df, row, column, value=False, OR='yes', RR='yes'):
    """
    2x2 table of disease and exposure

    PARAMETERS
    -----------------------
    row = name of exposure row as string
    column = name of outcome column as string
    value = optional, if column values need to be filtered

    RETURNS
    ------------------------
    pandas dataframe of 2x2 table. Prints odds ratio and relative risk.

    TODO
    ------------------------
    would be nice to add:
    [] confidence intervals for RR
    [] chi square and p value
    """
    
    if value == False:
        table = pd.DataFrame(pd.crosstab(df[row], df[column], margins=True))
    else:
        table = pd.DataFrame(pd.crosstab(df[row], df[column][df[column]==value], margins=True))

    a = table.ix[0][0]
    b = table.ix[0][1]
    c = table.ix[1][0]
    d = table.ix[1][1]

    if OR == 'yes':
        ratio = (a*d)/(b*c)
        or_se = np.sqrt((1/a)+(1/b)+(1/c)+(1/d))
        _or_LCI = np.log(ratio)-1.96*or_se
        _or_UCI = np.log(ratio)+1.96*or_se
        or_LCI = round(np.exp(_or_LCI), 2)
        or_UCI = round(np.exp(_or_UCI), 2)
        
        print 'Odds ratio: {} (95% CI: {}, {})'.format(round(ratio, 2), or_LCI, or_UCI)
        
    if RR == 'yes':
        rr = (a/(a+b))/(c/(c+d))
        print 'Relative risk: ', rr

    return table



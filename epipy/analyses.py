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


def two_x_two(df, row, column, row_order, col_order):
    """
    2x2 table of disease and exposure

    PARAMETERS
    -----------------------
    row = name of exposure row as string
    column = name of outcome column as string
    row_order = list of rows
    col_order = list of columns

    RETURNS
    ------------------------
    pandas dataframe of 2x2 table. Prints odds ratio and relative risk.

    TODO
    ------------------------
    [] organize cols and rows in yes/no order
    [] chi square and p value
    """
    if type(col_order) != list or type(row_order) != list:
        raise TypeError('columns and rows must be lists')
        
    if len(col_order) != 2 or len(row_order) != 2:
        raise AssertionError('must have two columns and two rows')

    _table = pd.crosstab(df[row], df[column], margins=True).to_dict()

    trow = row_order[0]
    brow = row_order[1]
    tcol = col_order[0]
    bcol = col_order[1]
    
    table = pd.DataFrame(_table, index=[trow, brow, 'All'], columns=[tcol, bcol, 'All'])

    a = table.ix[0][0]
    b = table.ix[0][1]
    c = table.ix[1][0]
    d = table.ix[1][1]

    ratio = (a*d)/(b*c)
    or_se = np.sqrt((1/a)+(1/b)+(1/c)+(1/d))
    or_ci = conf_interval(ratio, or_se)
    print 'Odds ratio: {} (95% CI: {})'.format(round(ratio, 2), or_ci)
        
    rr = (a/(a+b))/(c/(c+d))
    rr_se = np.sqrt(((1/a)+(1/c)) - ((1/(a+b)) + (1/(c+d))))
    rr_ci = conf_interval(rr, rr_se)
    print 'Relative risk: {} (95% CI: {})'.format(round(rr, 2), rr_ci)

    return table


def conf_interval(ratio, std_error):
    _lci = np.log(ratio) - 1.96*std_error
    _uci = np.log(ratio) + 1.96*std_error

    lci = round(np.exp(_lci), 2)
    uci = round(np.exp(_uci), 2)

    return (lci, uci)

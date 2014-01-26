#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
from scipy.stats import chi2_contingency
import pandas as pd
import matplotlib.pyplot as plt

def _get_table_labels(table):
    """
    Returns classic a, b, c, d labels for contingency table calcs.
    """
    a = table[0][0]
    b = table[0][1]
    c = table[1][0]
    d = table[1][1]

    return a, b, c, d


def _ordered_table(table):
    """
    Determine type of table input. Find classic a, b, c, d labels
    for contigency table calculations.
    """
    if type(table) is list:
        a, b, c, d = _get_table_labels(table)
    elif type(table) is pd.core.frame.DataFrame:
        a, b, c, d = _get_table_labels(table.values)
    elif type(table) is np.ndarray:
        a, b, c, d = _get_table_labels(table)
    else:
        raise TypeError('table format not recognized')

    return a, b, c, d


def _conf_interval(ratio, std_error):
    """
    Calculate 95% confidence interval for odds ratio and relative risk.
    """
    
    _lci = np.log(ratio) - 1.96*std_error
    _uci = np.log(ratio) + 1.96*std_error

    lci = round(np.exp(_lci), 2)
    uci = round(np.exp(_uci), 2)

    return (lci, uci)


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


def create_2x2(df, row, column, row_order, col_order):
    """
    2x2 table of disease and exposure in traditional epi order.

    Table format:
                Disease
    Exposure    YES     NO
    YES         a       b
    NO          c       d

    PARAMETERS
    -----------------------
    row = name of exposure row as string
    column = name of outcome column as string
    row_order = list of length 2 of row values in yes/no order.
                Example: ['Exposed', 'Unexposed']
    col_order = list of length 2 column values in yes/no order.
                Example: ['Sick', 'Not sick']

    RETURNS
    ------------------------
    pandas dataframe of 2x2 table. Prints odds ratio and relative risk.
    """
    if type(col_order) != list or type(row_order) != list:
        raise TypeError('row_order and col_order must each be lists of length 2')
        
    if len(col_order) != 2 or len(row_order) != 2:
        raise AssertionError('row_order and col_order must each be lists of length 2')

    _table = pd.crosstab(df[row], df[column], margins=True).to_dict()

    trow = row_order[0]
    brow = row_order[1]
    tcol = col_order[0]
    bcol = col_order[1]
    
    table = pd.DataFrame(_table, index=[trow, brow, 'All'], columns=[tcol, bcol, 'All'])
    a, b, c, d = _ordered_table(table)

    return table


def analyze_2x2(table):
    """Prints odds ratio, relative risk, and chi square.
    See also create_2x2(), odds_ratio(), relative_risk(), and chi2()

    PARAMETERS
    --------------------
    2x2 table as pandas dataframe, numpy array, or list in format [a, b, c, d]

    Table format:
                Disease
    Exposure    YES     NO
    YES         a       b
    NO          c       d
    
    """
    odds_ratio(table)
    relative_risk(table)
    chi2(table)


def odds_ratio(table):
    """
    Calculates the odds ratio and 95% confidence interval. See also
    analyze_2x2()

    PARAMETERS
    ----------------------
    table = accepts pandas dataframe, numpy array, or list in [a, b, c, d] format.

    RETURNS
    ----------------------
    returns and prints odds ratio and tuple of 95% confidence interval
    """
    a, b, c, d = _ordered_table(table)

    ratio = (a*d)/(b*c)
    or_se = np.sqrt((1/a)+(1/b)+(1/c)+(1/d))
    or_ci = _conf_interval(ratio, or_se)
    print 'Odds ratio: {} (95% CI: {})'.format(round(ratio, 2), or_ci)

    return round(ratio, 2), or_ci

    
def relative_risk(table):
    """
    Calculates the relative risk and 95% confidence interval. See also
    analyze_2x2().
    
    PARAMETERS
    ----------------------
    table = accepts pandas dataframe, numpy array, or list in [a, b, c, d] format.

    RETURNS
    ----------------------
    returns and prints relative risk and tuple of 95% confidence interval
    """
    a, b, c, d = _ordered_table(table)
    
    rr = (a/(a+b))/(c/(c+d))
    rr_se = np.sqrt(((1/a)+(1/c)) - ((1/(a+b)) + (1/(c+d))))
    rr_ci = _conf_interval(rr, rr_se)
    print 'Relative risk: {} (95% CI: {})\n'.format(round(rr, 2), rr_ci)

    return rr, rr_ci


def chi2(table):
    """
    Scipy.stats function to calculate chi square.
    PARAMETERS
    ----------------------
    table = accepts pandas dataframe or numpy array. See also
    analyze_2x2().

    RETURNS
    ----------------------
    returns chi square with yates correction, p value,
    degrees of freedom, and array of expected values.
    prints chi square and p value
    """
    chi2, p, dof, expected = chi2_contingency(table)
    print 'Chi square: {}'.format(chi2)
    print 'p value: {}'.format(p)

    return chi2, p, dof, expected





    

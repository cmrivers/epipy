# usr/bin/python
# -*- coding: utf-8 -*-
'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
  '''
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot
import epipy as epi


def or_plot(df, risk_cols, outcome_col):
    """
    df = pandas dataframe of line listing
    cols = list of columns to include in analysis

    # Order of operations #
    + read in dataframe or series
    + for each column
    + send to create_2x2
    -send to odds_ratio
    -plot OR on scatterplot
    -color by OR
    -plot CI on scatterplot
    """
    for col in risk_cols:
        risk_order = ["{}".format(val) for val in risk_cols.values()]
        outcome_order = ["{}".format(val) for val in outcome_col.values()]
        table = epi.create_2x2(df, "{}".format(col), "{}".format(outcome_col), risk_order, outcome_order)
        ratio, or_ci = epi.odds_ratio(table)






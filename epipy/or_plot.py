# usr/bin/python
# -*- coding: utf-8 -*-

'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
  '''

import pandas as pd
from matplotlib.pyplot import plt
import analyses

def _plot(ratios):
    """
    """

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect('auto')
    ax.set_ylabel('Odds ratio')
    ax.grid(True)

    for ratio in ratios:



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

    ratio_pairs = []
    for col in df.itercols(): #this part isn't right...I forget how to select cols efficiently
        if col.index in risk_cols:
            risk_order = ["{}".format(val) for val in risk_cols.values()]
            outcome_order = ["{}".format(val) for val in outcome_col.values()]
            table = analyses.create_2x2(df, "{}".format(col), "{}".format(outcome_col), risk_order, outcome_order)
            ratio, or_ci = epi.odds_ratio(table)
            ratio_pairs.append({name:col.index, ratio:ratio, ci:or_ci})

    _plot(ratio_pairs)









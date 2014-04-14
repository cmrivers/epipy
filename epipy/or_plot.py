# usr/bin/python
# -*- coding: utf-8 -*-

'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
  '''

import pandas as pd
import matplotlib.pyplot as plt
import analyses

def _plot(names, ratio, ci):
    """
    """

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect('auto')
    ax.set_ylabel('Odds ratio')
    ax.grid(True)

    yvalues = range(len(names))
    ax.scatter(ratio, yvalues)
    textspot = x1 + timedelta((x2 - x1).days/2.0, 0, 0)



def or_plot(df, risk_cols, outcome_col):
    """
    df = pandas dataframe of line listing
    cols = list of columns to include in analysis

    # Order of operations #
    + read in dataframe or series
    + for each column
    + send to create_2x2
    + send to odds_ratio
    -plot OR on scatterplot
    -color by OR
    -plot CI on scatterplot
    """

    names = []
    ratio = []
    ci = []
    for risk_col in risk_cols:
        risk_order = ["{}".format(val) for val in df[risk_col].unique()]
        outcome_order = ["{}".format(val) for val in df[outcome_col].unique()]
        table = epi.create_2x2(df, "{}".format(risk_order), "{}".format(outcome_order), risk_order, outcome_order)
        ratio, or_ci = epi.odds_ratio(table)
        names.append(col.index)
        ratio.append(ratio)
        ci.append(or_ci)

    _plot(names, ratio, ci)









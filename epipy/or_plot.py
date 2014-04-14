# usr/bin/python
# -*- coding: utf-8 -*-

'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
  Modify to handle nonstring values
  '''

import pandas as pd
import matplotlib.pyplot as plt
import analyses

def _plot(ratios):
    """
    """
    df = pd.DataFrame(df)
    df = df.sort('ratio')

    fig, ax = plt.subplots()
    ax.set_aspect('auto')
    ax.set_xlabel('Odds ratio')
    ax.grid(True)

    nnames = len(df)
    ypos = range(nnames)
    ax.set_ylim(-.5, nnames - .5)
    plt.yticks(ypos)

    ax.scatter(df.ratio, ypos)
    for pos in ypos:
        ax.fill_between([df.lower[pos], df.upper[pos]], pos, pos+.01, color='b', alpha=.3)

    ax.set_yticklabels(df.names)

    return fig, ax



def or_plot(df, risk_cols, outcome_col):
    """
    df = pandas dataframe of line listing
    cols = list of columns to include in analysis
    """

    ratio_df = []
    for risk_col in risk_cols:
        risk_order = ["{}".format(val) for val in df[risk_col].unique()]
        outcome_order = ["{}".format(val) for val in df[outcome_col].unique()]
        table = epi.create_2x2(df, risk_col, outcome_col, risk_order, outcome_order)
        ratio, or_ci = epi.odds_ratio(table)
        ratio_df.append({'names': risk_col, 'ratio':ratio, 'lower':or_ci[0], 'upper':or_ci[1]})

    fig, ax = _plot(ratio_df)









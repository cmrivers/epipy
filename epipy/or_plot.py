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

def _plot(_df):
    """
    """

    _df = pd.DataFrame(_df)
    df = _df.sort('ratio')
    df['color'] = 'grey'
    df.color[(df.lower > 1) & (df.upper > 1)] = 'blue'
    df.color[(df.lower < 1) & (df.upper < 1)] = 'red'

    df.index = range(len(df))  # reset the index to reflect order

    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_aspect('auto')
    ax.set_xlabel('Odds ratio')
    ax.grid(False)
    ax.set_ylim(-.5, len(df) - .5)
    plt.yticks(df.index)

    ax.scatter(df.ratio, df.index, c=df.color, s=50)
    for pos in range(len(df)):
        ax.fill_between([df.lower[pos], df.upper[pos]], pos-.01, pos+.01, color='grey', alpha=.3)

    ax.set_yticklabels(df.names)
    ax.vlines(x=1, ymin=-.5, ymax=len(df)-.5, colors='grey', linestyles='--')
    return fig, ax



def or_plot(df, risk_cols, outcome_col, risk_order, outcome_order):
    """
    df = pandas dataframe of line listing
    cols = list of columns to include in analysis
    """

    ratio_df = []
    cnt = 1
    for risk_col in risk_cols:
        #if risk_order == False:
        #    risks = ["{}".format(val) for val in df[risk_col].dropna().unique()]
        #    outcome_order = ["{}".format(val) for val in df[outcome_col].dropna().unique()]
        #else:
        #outcome_order = risk_order[0]
        #risks = risk_order[cnt]

        table = analyses.create_2x2(df, risk_col, outcome_col, outcome_order, risk_order)
        ratio, or_ci = analyses.odds_ratio(table)
        ratio_df.append({'names': risk_col, 'ratio':ratio, 'lower':or_ci[0], 'upper':or_ci[1]})

        cnt += 1

    fig, ax = _plot(ratio_df)









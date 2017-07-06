# usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import analyses


def _plot(_df, fig, ax):
    """
    """

    _df = pd.DataFrame(_df)
    df = _df.sort('ratio')
    df['color'] = 'grey'
    df.color[(df.lower > 1) & (df.upper > 1)] = 'blue'
    df.color[(df.lower < 1) & (df.upper < 1)] = 'red'

    df.index = range(len(df))  # reset the index to reflect order

    if fig is None and ax is None:
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


def or_plot(df, risk_cols, outcome_col, risk_order, outcome_order, fig=None, ax=None):
    """
    df = pandas dataframe of line listing
    cols = list of columns to include in analysis
    risk_order: dictionary with risk_cols as keys, and a list of values as values, e.g. {'sex':['male', 'female']}
    outcome_order: list of values, e.g. ['alive', 'dead']
    
    RETURNS
    --------
    fig, ax = figure and axis objects
    """

    ratio_df = []

    for risk_col in risk_cols:
      #  if risk_order != False:
        order = risk_order[risk_col]

        #elif risk_order == False:
        #    risks = ["{}".format(val) for val in df[risk_col].dropna().unique()]
        #    outcome_order = ["{}".format(val) for val in df[outcome_col].dropna().unique()]

        _df = df[[outcome_col, risk_col]].dropna(how='any')

        if len(_df[outcome_col].unique()) > 2:
            raise Exception('More than two unique values in the outcome')

        if len(_df[risk_col].unique()) > 2:
            raise Exception('More than two unique values in {}'.format(risk_col))


        table = analyses.create_2x2(_df, risk_col, outcome_col, order, outcome_order)
        print('{}:'.format(risk_col))
        ratio, or_ci = analyses.odds_ratio(table)
        print('\n')


        ratio_df.append({'names': risk_col, 'ratio':ratio, 'lower':or_ci[0], 'upper':or_ci[1]})

    fig, ax = _plot(ratio_df, fig, ax)

    return fig, ax

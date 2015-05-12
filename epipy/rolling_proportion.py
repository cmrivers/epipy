import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def rolling_proportion(df, date_col, value_col, value, window=30, dropna=True, label=False, fig=None, ax=None):
    """
    df = pandas df
    date_col = name of column containing dates
    value_col = name of column to be tallied
    value = value to tally (e.g. 'Male')
    window = number of days to include. Default is 30.
    dropna = exclude rows where val is NaN. Default is true. False will include those rows.
    label = legend label
    fig, ax = matplotlib objects
    -----
    Returns Series of proportions with date index, fig, and ax.
    -----
    Example:
    datetime_df.index = df.dates
    rolling_proportion(datetime_df.sex, 'Male')

    Note: If you are having trouble, make ensure that your date_col is a datetime.
    """

    df = df[df[date_col].isnull() == False]
    df.index = df[date_col]

    if dropna == False:
        df = df[value_col].fillna(False)
    else:
        df = df[df[value_col].isnull() == False]

    df['matches'] = df[value_col] == value
    df['matches'] = df['matches'].astype(np.int)
    df['ones'] = 1

    prop = pd.DataFrame()
    prop['numerator'] = df.matches.groupby(by=df.index).sum()
    prop['denom'] = df.ones.groupby(by=df.index).sum()
    prop['proportion'] = pd.rolling_sum(prop.numerator, window, 5)/pd.rolling_sum(prop.denom, window, 5)
    prop = prop.dropna(how='any')

    ts = pd.date_range(min(prop.index), max(prop.index))
    new_prop = prop['proportion']
    new_prop = new_prop.reindex(ts)
    new_prop = new_prop.fillna(method='pad')

    if fig is None and ax is None:
        fig, ax = plt.subplots()

    ax.xaxis_date()
    new_prop.plot(ax=ax, label=label)
    fig.autofmt_xdate()
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel('')
    if label != False:
        ax.legend()

    return new_prop, fig, ax

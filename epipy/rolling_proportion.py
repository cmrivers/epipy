import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def rolling_proportion(Series, val, window=30, dropna=True, label=False, fig=None, ax=None):
    """
    Series = pandas Series with DatetimeIndex
    val = value to tally
    window = number of days to include. Default is 30.
    dropna = exclude rows where val is NaN. Default is true. False will include those rows.
    label = legend label
    fig, ax = matplotlib objects

    Example:
    datetime_df.index = df.dates
    rolling_proportion(datetime_df.sex, 'Male')
    """
    if dropna == False:
        df = pd.DataFrame(Series).fillna(False)
    else:
        df = pd.DataFrame(Series.dropna())

    df['matches'] = df == val
    df['matches'] = df['matches'].astype(np.int)
    df['ones'] = 1

    prop = pd.DataFrame(df.matches.groupby(by=df.index).sum(), columns=['numerator'])
    prop['denom'] = df.ones.groupby(by=df.index).sum()
    prop['proportion'] = pd.rolling_sum(prop.numerator, window, 5)/pd.rolling_sum(prop.denom, window, 5)

    ts = pd.date_range(min(df.index), max(df.index))

    prop = prop.reindex(ts)
    prop.proportion = prop.proportion.fillna(method='pad')

    if fig == None:
        fig, ax = plt.subplots(sharex=True)

    ax.xaxis_date()
    prop.proportion.plot(ax=ax, label=label)
    fig.autofmt_xdate()
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel('')
    if label != False:
        ax.legend()

    return fig
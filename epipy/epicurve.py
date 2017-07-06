#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt


def epicurve_plot(df, date_col, freq, fig= None, ax=None, color=None):
    '''
    Creates an epicurve (count of new cases over time)

    df = pandas dataframe
    date_col = date used to denote case onset or report date
    freq = desired plotting frequency. Can be day (d), month (m) or year (y)
    fig, ax = fig & ax objects
    color = value of bar color to be passed to matplotlib
    
    RETURNS
    ------------------
    curve = Series of dates and counts
    fig, ax = matplotlib figure and axis objects
    '''

    if ax == None:
        fig, ax = plt.subplots()

    df = df[df[date_col].isnull() == False]
    freq = freq.lower()[0]

    ix = pd.date_range(df[date_col].min(), df[date_col].max(), freq='d')

    curve = pd.DataFrame(df[date_col].value_counts().sort_index())
    
    if freq == 'm' or freq == 'd':
        curve = curve.reindex(ix).fillna(0).resample(freq, how='sum', closed='right')
    if freq == 'y':
        curve = curve.groupby(curve.index.year).sum()
    
    curve = curve.rename(columns={date_col:'counts'})

    fig, ax = _plot(curve, freq, fig, ax, color='#53B8DD')

    return curve, fig, ax


def _plot(freq_table, freq, fig, ax, color):
    '''
    Plot number of new cases over time
    freq_table = frequency table of cases by date, from epicurve()
    freq = inherited from epicurve
    '''

    # care about date formatting
    if freq == 'd':
        ax.xaxis_date()
        fig.autofmt_xdate()
        ax.bar(freq_table.index.values, freq_table['counts'].values, align='center', color=color)

    elif freq == 'm':
        if len(freq_table) < 5:
            freq_table.index = freq_table.index.strftime('%b %Y')
            freq_table.plot(kind='bar', rot=0, legend=False, color=color)
        else: 
            ax.xaxis_date()
            fig.autofmt_xdate()
            ax.bar(freq_table.index.values, freq_table['counts'].values, align='center',width=5, color=color)

    elif freq == 'y':
       freq_table.plot(kind='bar', rot=0, legend=False, color=color)
       
    return fig, ax
        
    
        
    
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import epipy
import pandas as pd
import matplotlib.pyplot as plt


def epicurve_plot(df, date_col, freq, fig= None, ax=None, color=None):
    '''
    Creates an epicurve (count of new cases over time)

    df = pandas dataframe
    date_col = date used to denote case onset or report date
    freq = desired plotting frequency. Can be day, month or year
    title = optional
    fig, ax = fig ax objects
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
    ix = pd.date_range(df[date_col].min(), df[date_col].max(), freq=freq)
    
    if freq == 'd':
        curve = pd.DataFrame(df[date_col].value_counts().sort_index())

    elif freq == 'm':
        curve = pd.DataFrame(df[date_col].value_counts().sort_index())
        curve = curve.resample(freq, how='sum')

    elif freq == 'y':
        df.new_col = df.new_col.dropna().map(lambda x: x.year)
        curve = pd.DataFrame(df.new_col.value_counts())
    
    curve = curve.reindex(ix).fillna(0)
    curve = curve.rename(columns={date_col:'counts'})

    fig, ax = _plot(curve, freq, fig, ax, color)

    return curve, fig, ax


def _plot(freq_table, freq, fig, ax, color):
    '''
    Plot number of new cases over time
    freq_table = frequency table of cases by date, from epicurve()
    freq = inherited from epicurve
    '''

    axprop =  ax.axis()

    # care about date formatting
    if freq == 'd':
        #wid = ((2*axprop[1]-axprop[0])/axprop[1])
        ax.xaxis_date()
        fig.autofmt_xdate()

    elif freq == 'm':
        ax.xaxis_date()
        fig.autofmt_xdate()
        #wid = len(freq_table)

    elif freq == 'y':
        locs = freq_table.index.tolist()
        labels = [str(loc) for loc in locs]
        #wid = 1
        ax.set_xticks(locs)
        ax.set_xticklabels(labels)

    if color == None:
        color == 'b'
        
    ax.bar(freq_table.index, freq_table['counts'].values, align='center', color=color)

    return fig, ax

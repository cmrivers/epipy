#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
 Epicurve creates weekly, monthly, or daily epicurves
 (count of new cases over time) from a line list.
'''
from __future__ import division
import epipy
from .basics import date_convert
import pandas as pd
import matplotlib.pyplot as plt


def epicurve_plot(df, date_col, freq, title=None, fig= None, ax=None):
    '''
    Creates an epicurve (count of new cases over time)

    df = pandas dataframe
    date_col = date used to denote case onset or report date
    freq = desired plotting frequency. Can be day, month or year
    title = optional
    date_format = datetime string format, default is "%Y-%m-%d"
    '''

    if ax == None
        fig, ax = plt.subplots()

    df = df[df[date_col].isnull() == False]
    freq = freq.lower()[0]
    df.new_col = df[date_col]

    #count the number of cases per time period
    if freq == 'd':
        curve = pd.DataFrame(df[date_col].value_counts(), columns=['count'])

    elif freq == 'm':
	#convert dates to months
        format_date = df.new_col.dropna().map(lambda x: str(x.strftime("%Y/%m")))
        form = format_date.map(lambda x: date_convert(x, "%Y/%m"))
	#count number of cases per month
        curve = pd.DataFrame(form.value_counts(), columns=['count'])

    elif freq == 'y':
	#convert dates to year
        df.new_col = df.new_col.dropna().map(lambda x: x.year)
	#count number of cases per year
        curve = pd.DataFrame(df.new_col.value_counts(), columns=['count'])

    _plot(curve, freq, fig, ax, title)

    return curve, fig, ax


def _plot(freq_table, freq, fig, ax, title=None):
    '''
    Plot number of new cases over time
    freq_table = frequency table of cases by date, from epicurve()
    freq = inherited from epicurve
    '''

    axprop =  ax.axis()
    freq_table['plotdates'] = freq_table.index

    # care about date formatting
    if freq == 'd':
        wid = ((2*axprop[1]-axprop[0])/axprop[1])
        ax.xaxis_date()
        fig.autofmt_xdate()

    elif freq == 'm':
        ax.xaxis_date()
        fig.autofmt_xdate()
        wid = len(freq_table)

    elif freq == 'y':
        locs = freq_table['plotdates'].values.tolist()
        labels = [str(loc) for loc in locs]
        wid = 1
        ax.set_xticks(locs)
        ax.set_xticklabels(labels)

    ax.bar(freq_table['plotdates'].values, freq_table['count'].values,
	width=wid, align='center')

    if title != None:
        ax.set_title(title)

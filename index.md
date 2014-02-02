---
layout: page
title: Quick start!
tagline: Getting started with epipy
---
{% include JB/setup %}

Epipy is a Psython package for epidemiology.  It contains (or will contain...)
tools for analyzing and visualizing epidemiology data. Epipy can currently produce:

* stratified summary statistics
* case tree and checkerboard plots
* epidemic curves plots
* analysis of case attribute (e.g. sex) by generation
* 2x2 tables with odds ratio and relative risk
* summary of cluster basic reproduction numbers

Installation
------------
To install epipy, clone the repository and install using setup.py:

    git clone https://github.com/cmrivers/epipy.git
    python setup.py install

Quickstart
------------
**Case tree plot**

    import epipy
    import os

    df = pd.read_csv('epipy/data/example_data.csv')
    fig, ax = epipy.case_tree_plot(df, 'Cluster', 'ID', 'Date', 5, 4, 'Cluster')

![Casetree plot](http://github.com/cmrivers/epipy/blob/master/figs/example_casetree.png?raw=true)


**Checkerboard plot**

    fig, ax = epipy.checkerboard_plot(df, 'ID', 'Cluster', 'Date')

![Checkerboard plot](https://github.com/cmrivers/epipy/blob/master/figs/test_checkerboard.png?raw=true)


**Epidemic curve**

    mers_df = pd.read_csv('epipy/data/mers_line_list.csv')
    plt.figure()
    epipy.epicurve_plot(mers_df, date_col='dates', freq='m')

![Daily epicurve](https://github.com/cmrivers/epipy/blob/master/figs/month_epicurve.png?raw=true)

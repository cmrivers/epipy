---
layout: page
title: Epipy
tagline: Python tools for epidemiology
---
{% include JB/setup %}

Epipy is a Python package for epidemiology.  It contains (or will contain...)
tools for analyzing and visualizing epidemiology data. Epipy can currently produce:

* stratified summary statistics
* [case tree](http://cmrivers.github.io/epipy/plots/2014/02/01/case-tree-plot/) and [checkerboard plots](http://cmrivers.github.io/epipy/plots/2014/02/01/checkerboard-plot/)
* [epidemic curves plots](http://cmrivers.github.io/epipy/plots/2014/02/01/epicurves/)
* analysis of case attribute (e.g. sex) by generation
* 2x2 tables with odds ratio and relative risk
* summary of cluster basic reproduction numbers

Installation
------------
To install epipy, clone the repository and install using setup.py:

    git clone https://github.com/cmrivers/epipy.git
    python setup.py install


Note that I use the package [mpltools](http://tonysyu.github.io/mpltools/) to produce the nice ggplot-style plot aesthetics you see in my examples. Using mpltools is optional, but I highly recommend it.


Quickstart
------------
**Case tree plot**

    import epipy as epi
    import pandas as pd

    df = pd.read_csv('epipy/data/example_data.csv')
    fig, ax = epi.case_tree_plot(example_df, cluster_id = 'Cluster', \
              case_id ='ID', date_col='Date', color='Cluster', \
              gen_mean=4, gen_sd = 1)
    ax.set_title('Example outbreak data')

![Casetree plot](http://github.com/cmrivers/epipy/blob/master/figs/example_casetree.png?raw=true)


**Checkerboard plot**

    fig, ax = epi.checkerboard_plot(df, 'ID', 'Cluster', 'Date')
    ax.set_title('Example outbreak data')

![Checkerboard plot](https://github.com/cmrivers/epipy/blob/master/figs/test_checkerboard.png?raw=true)


**Epidemic curve**

    mers_df = pd.read_csv('epipy/data/mers_line_list.csv')
    curve, fig, ax = epi.epicurve_plot(mers_df, date_col='dates', freq='m')
    ax.set_title('Approximate onset or report date of MERS cases')

![Daily epicurve](https://github.com/cmrivers/epipy/blob/master/figs/month_epicurve.png?raw=true)

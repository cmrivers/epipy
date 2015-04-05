---
layout: page
title: Introduction
tagline: Python tools for epidemiology
---
{% include JB/setup %}

Epipy is a Python package for epidemiology. It contains tools for analyzing and visualizing epidemiology data. Epipy can currently produce:

* [stratified summary statistics](http://cmrivers.github.io/epipy/analyses/2014/02/02/basic-epidemiology/)
* [case trees](http://cmrivers.github.io/epipy/plots/2014/02/01/case-tree-plot/) and [checkerboard plots](http://cmrivers.github.io/epipy/plots/2014/02/01/checkerboard-plot/)
* [epicurves](http://cmrivers.github.io/epipy/plots/2014/02/01/epicurves/)
* [analysis of case attribute (e.g. sex) by generation](http://cmrivers.github.io/epipy/analyses/2014/02/02/basic-epidemiology/)
* [easily create 2x2 tables](http://cmrivers.github.io/epipy/analyses/2014/02/02/basic-epidemiology/)
* produce odds ratios, attributable risk, diagnostic accuracy, kappa agreement, and relative risk for 2x2 tables
* [summary of cluster basic reproduction numbers](http://cmrivers.github.io/epipy/analyses/2014/02/02/basic-epidemiology/)
* odds ratio plots^
* rolling proportion plots^
^dev version only


Installation
------------
Install using pip:

    pip install epipy

or clone the [github repository](http://github.com/cmrivers/epipy) and install using setup.py:

    git clone https://github.com/cmrivers/epipy.git
    python setup.py install

Note that I use the package [seaborn](stanford.edu/~mwaskom/software/seaborn/) to produce the nice ggplot-style plot aesthetics you see in my examples. Using mpltools is optional, but I highly recommend it.


Quickstart
------------
**Case tree plot**

    import epipy as epi
    import pandas as pd

    # optional import
    import seaborn as sns

    example_df = epi.get_data('example_data')
    fig, ax = epi.case_tree_plot(example_df, cluster_id = 'Cluster', \
              case_id ='ID', date_col='Date', color='Cluster', \
              gen_mean=4, gen_sd = 1)
    ax.set_title('Example outbreak data')

![Casetree plot](http://github.com/cmrivers/epipy/blob/master/figs/example_casetree.png?raw=true)

**Generation analysis**

    mers_df = epi.get_data('mers_line_list')
    mers_G = epi.build_graph(mers_df, cluster_id='Cluster ID', case_id='Case #',
		        date_col='dates', color='Health status', gen_mean=5, gen_sd=4)
    fig, ax, table = epi.generation_analysis(mers_G, attribute='Health status', \
                                             plot=True)


table returns:

    Health status  Alive  Asymptomatic  Critical  Dead  Mild  Recovered  All
    generation
    0                  5             1         3    12     1          0   22
    1                  6             7         3    10     8          0   35
    2                  2             5         2     7     2          2   20
    3                  0             5         4     5     0          2   16
    4                  1             0         0     2     0          0    3
    5                  0             0         0     1     0          0    1
    6                  1             0         0     1     0          0    2
    7                  1             0         0     0     0          0    1
    8                  0             0         0     0     0          1    1
    All               16            18        12    38    11          5  101

![Health status by generation](https://github.com/cmrivers/epipy/blob/master/figs/mers_generation_hist.png?raw=true)


**Epidemic curve**

    curve, fig, ax = epi.epicurve_plot(mers_df, date_col='dates', freq='m')
    ax.set_title('Approximate onset or report date of MERS cases')

![Daily epicurve](https://github.com/cmrivers/epipy/blob/master/figs/month_epicurve.png?raw=true)


**Stratified summary statistics**

    df = pd.DataFrame({'Age' : [10, 12, 14], 'Group' : ['A', 'B', 'B'] })
    epi.summary(df.Age, by=df.Group)

returns:

        count  missing  min  median  mean      std   max
    A      1        0   10      10    10       NaN   10
    B      2        0   12      13    13  1.414214   14


Next: see an [example with outbreak data](http://cmrivers.github.io/epipy/mers.html) or read the [documentation](http://cmrivers.github.io/epipy/categories.html)

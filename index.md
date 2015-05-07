---
layout: page
title: Epipy
tagline: Python tools for epidemiology
---
{% include JB/setup %}


Epipy is a Python package for epidemiology. It contains tools for analyzing and visualizing epidemiology data.

To check out the code, report a bug, or contribute features, visit [github](http://github.com/cmrivers/epipy), or visit me on [twitter](www.twitter.com/cmyeaton).

Installation
------------
Install using pip:

    pip install epipy

or clone the [github repository](http://github.com/cmrivers/epipy) and install using setup.py:

    git clone https://github.com/cmrivers/epipy.git
    python setup.py install


Note that I use the package [seaborn](http://stanford.edu/~mwaskom/software/seaborn/) to produce the nice plot aesthetics you see in my examples. Using seaborn is optional, but I highly recommend it.


Documentation
------------

##Basic epidemiology

* [Summary statistics](cmrivers.github.io/epipy/analyses/2015/05/07/summarystats.md)
* [2x2 table](cmrivers.github.io/epipy/analyses/2015/05/07/summarystats.md)
  * Odds ratio
  * Relative risk
  * Attributable risk
  * Chi square
  * Diagnostic accuracy
* [Cluster analysis]

##Plotting

* Case tree plot
* Checkerboard plot
* Epicurves
* Odds ratio plot
* Rolling proportion plot
* Stripe plot
=======
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


![Casetree plot](https://github.com/cmrivers/epipy/blob/master/figs/example_casetree_health.png?raw=true)


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
>>>>>>> be31b9ecd28a7d6e609023c339da0e608034d5cd

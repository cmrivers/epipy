---
layout: post
category : analyses
tagline: "Case tree plot analyses"
tags : [analyses, case tree]
---
{% include JB/setup %}

[Case tree plots](http://cmrivers.github.io/epipy/plots/2014/02/01/case-tree-plot/) allow unusual insight into the dynamics of an outbreak. Epipy currently has two functions to analyze the emerging zoonoses that case tree plots were developed to represent.

##Basic reproduction number

**What is the basic reproduction number?**

The basic reproduction number, also called R0, is the average number of secondary cases each case produces in a fully susceptible population. In order for an outbreak to sustain itself, R0 must be greater than 1. The higher the R0, the more infectious the disease.

For most outbreaks, R0 must be estimated. Case tree plots have the advantage of showing the exact number of secondary cases per source case.

**Example**

We'll use data from the MERS-CoV outbreak that comes packaged with epipy. To start, we'll need to build out the graph. Then simply call reproduction_number(), which will return a series object, and a histogram of the R0s. The function has an option to exclude index cases (index_cases=False), which is usefuul if you want to calculate the human to human reproduction number without considering zoonotically acquired cases.

    import epipy as epi
    import pandas as pd

    mers_df = pd.read_csv('../data/mers_line_list.csv')
    mers_G = epi.build_graph(mers_df, cluster_id='Cluster ID', case_id='Case #',
		        date_col='dates', color='Health status', gen_mean=5, gen_sd=4)

    R, fig, ax = epi.reproduction_number(mers_G, index_cases=True, plot=True)


The series object, R in the above example, can be manipulated further.

    print R.describe()

The R variable returns:

    count    101.000000
    mean       1.000000
    std        1.296148
    min        0.000000
    25%        0.000000
    50%        0.000000
    75%        2.000000
    max        5.000000
    dtype: float64

And the figure returns:

![Histogram of reproduction numbers](https://github.com/cmrivers/epipy/blob/master/figs/r0_hist.png?raw=true)



##Generation analyses

Epidemiologists must also be interested in how the disease changes from one generation to the next. Are cases acquired from animals more severe than human acquired cases? Does severity decrease as the disease passes from person to person? Are index cases more likely to be men? The generation_analysis() function returns a table of case attributes by generation, as well as an optional bar graph.

**Example**

    fig, ax, table = epi.generation_analysis(mers_G, attribute='Health status', \
                                             plot=True)

The table variable returns:

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

And the figure returns:

![Health status by generation](https://github.com/cmrivers/epipy/blob/master/figs/mers_generation_hist.png?raw=true)
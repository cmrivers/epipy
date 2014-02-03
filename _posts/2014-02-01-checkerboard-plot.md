---
layout: post
category : plots
tagline: "Checkerboard plots"
tags : [plot, checkerboard]
---
{% include JB/setup %}

## Checkerboard plot

###What is a checkerboard plot?

I developed checkerboard plots to display similar data as a
[case tree plot](http://cmrivers.github.io/epipy/plots/2014/02/01/case-tree-plot/),
but instead of a network it shows a simple time series for each human to human cluster.
It does not attempt to determine the structure of the transmission network.


### Examples

First, load in the example data packaged with epipy (you may have to modify the path below).
Then simply call the checkerboard() function with column labels that correspond to columns
containing unique case id numbers, cluster membership, and the date of illness onset or report.
The label argument is optional; if set to off, no case id numbers will be displayed.

    import epipy as epi
    import pandas as pd

    df = pd.read_csv('epipy/data/example_data.csv')
    fig, ax = epi.checkerboard_plot(df, case_id='ID', cluster_id='Cluster', \
              date_col='Date', labels='on')
    ax.set_title('Example outbreak data')


![Checkerboard plot](https://github.com/cmrivers/epipy/blob/master/figs/test_checkerboard.png?raw=true)

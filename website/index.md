---
layout: page
title: Quick start!
tagline: Getting started with epipy
---
{% include JB/setup %}



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
    dir = os.path.dirname(__file__)

    df = pd.read_csv(os.path.join(dir, '../data/example_data.csv'))
    fig, ax = epipy.case_tree_plot(df, 'Cluster', 'ID', 'Date', 5, 4, 'Cluster')

![Casetree plot](http://github.com/cmrivers/epipy/blob/master/figs/example_casetree.png?raw=true)


**Checkerboard plot**

    fig, ax = epipy.checkerboard_plot(df, 'ID', 'Cluster', 'Date')

![Checkerboard plot](https://github.com/cmrivers/epipy/blob/master/figs/test_checkerboard.png?raw=true)


**Epidemic curve**

    mers_df = pd.read_csv(os.path.join(dir, '../data/mers_line_list.csv'))
    plt.figure()
    epipy.epicurve_plot(mers_df, date_col='dates', freq='m')

![Daily epicurve](https://github.com/cmrivers/epipy/blob/master/figs/month_epicurve.png?raw=true)

# FAQ
-----
###What is epipy?

Epipy is a python package for epidemiology.  It contains (or will contain...)
tools for analyzing and visualizing epidemiology data. Epipy can currently: generate case tree and checkerboard plots; analyze case attribute (e.g. sex) by generation; generate epidemic curves; produce 2x2 tables and find the odds ratio and relative risk; and generate a summary of cluster basic reproduction numbers.

###What is a case tree plot?

I came up with case tree plots as a way to visualize zoonotic disease.
However, it can also be used to visualizing environmentally-acquired
dieases, or anything that emerges multiple times, is passed from person
to person, and then dies out. Tweets and retweets might be a useful
non-epi example.

###How do I read a case tree plot?

The x axis is time of illness onset or diagnosis, and the y axis is
generation. Nodes at generation 0 are known as index nodes.
In the case of a zoonotic disease, the index node is a human case
acquired from an animal source. If that human were to pass
the disease to two other humans, those two subsequent cases are both
generation 1.

The meaning of the color of the node varies based on the node attribute.
In many cases, color just signifies membership to a particular human to
human cluster. However, it could also represent health status (e.g. alive, dead),
the sex of the patient, etc. 

###What is a checkerboard plot?

Checkerboard plots display similar data as a case tree plot, but instead
of a network it shows a simple time series for each human to human cluster.
It does not attempt to determine the structure of the transmission network.

The number in the center of each check is the case id that corresponds
to the the line listing. I have not yet figured out how to display these
numbers so they don't overlap. Sorry.

###I have a question/complaint/compliment.
Contact me at cmrivers@vbi.vt.edu, or @cmyeaton. Feel free to contribute!


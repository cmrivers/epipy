---
layout: post
category : plots
tagline: "Supporting tagline"
tags : [plot, case tree, checkerboard, epicurve]
---
{% include JB/setup %}

This Jekyll introduction will outline specifically  what Jekyll is and why you would want to use it.
Directly following the intro we'll learn exactly _how_ Jekyll does what it does.

## Case tree plot

###What is a case tree plot?

Case tree plots are a way to visualize zoonotic disease.
However, it can also be used to visualizing environmentally-acquired
dieases, or anything that emerges multiple times, is passed from person
to person, and then dies out. Tweets and retweets might be a useful
non-epi example.

###How do I read a case tree plot?

The x-axis is time of illness onset or diagnosis, and the y-axis is
generation. Nodes at generation 0 are known as index nodes.
In the case of a zoonotic disease, the index node is a human case
acquired from an animal source. If that human were to pass
the disease to two other humans, those two subsequent cases are both
generation 1.

The meaning of the color of the node varies based on the node attribute.
In many cases, color just signifies membership to a particular human to
human cluster. However, it could also represent health status (e.g. alive, dead), the sex of the patient, etc.

### Examples

First we will use example data packaged with epipy. We will color the nodes by their cluster.

    import epipy
    import os
    dir = os.path.dirname(__file__)

    df = pd.read_csv(os.path.join(dir, '../data/example_data.csv'))
    fig, ax = epipy.case_tree_plot(example_df, cluster_id = 'Cluster', \
                    case_id ='ID', date_col='Date', color='Cluster', \
                    gen_mean=4, gen_sd = 1)

![Casetree plot](http://github.com/cmrivers/epipy/blob/master/figs/example_casetree.png?raw=true)

If we want to change the node color to represent the health status of each case, we simply change the color argument.

    fig, ax = epipy.case_tree_plot(example_df, cluster_id = 'Cluster', \
                    case_id ='ID', date_col='Date', color='health', \
                    gen_mean=4, gen_sd = 1)
![Casetree plot](http://github.com/cmrivers/epipy/blob/master/figs/example_casetree_health.png?raw=true




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

**Basic epidemiology**

* [Summary statistics](cmrivers.github.io/epipy/analyses/2015/05/07/summarystats.md)
* [2x2 table](cmrivers.github.io/epipy/analyses/2015/05/07/summarystats.md)
  * Odds ratio
  * Relative risk
  * Attributable risk
  * Chi square
  * Diagnostic accuracy
* [Cluster + case tree analysis](http://cmrivers.github.io/epipy/analyses/2015/05/07/case-tree-analyses/)

**Plotting**

* [Case tree plot](http://cmrivers.github.io/epipy/plots/2015/05/11/case-tree-plot/)
* [Checkerboard plot](http://cmrivers.github.io/epipy/plots/2015/05/11/checkerboard-plot/)
* [Epicurves](http://cmrivers.github.io/epipy/plots/2015/05/11/epicurves/)
* [Odds ratio plot](http://cmrivers.github.io/epipy/plots/2015/05/11/odds-ratio-plot/)
* [Rolling proportion plot](http://cmrivers.github.io/epipy/plots/2015/05/11/rolling-proportion-plot/)
* [Steppe plot](http://cmrivers.github.io/epipy/plots/2015/05/11/steppe-plot/)

![Example case tree](https://github.com/cmrivers/epipy/blob/master/figs/example_case_tree.png?raw=true)


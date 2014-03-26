---
layout: page
title: "MERS-CoV case tree"
---
{% include JB/setup %}

I have been collecting a line list of MERS cases using publicly available data
like [WHO Disease Outbreak News reports](http://www.who.int/csr/don/en/).
Where possible, I've been trying to piece together human to human clusters -
it's guess-work at best, and I can't promise it's anything close to being correct.

The x-axis is time of illness onset or diagnosis, and the y-axis is generation.
Nodes at generation 0 are thought to be acquired from an animal source. If that
 human were to pass the disease to two other humans, those two subsequent cases
 are both generation 1.

Learn more about [case tree plots](http://cmrivers.github.io/epipy/plots/2014/02/01/case-tree-plot/)
or visit the full [MERS-CoV example](http://cmrivers.github.io/epipy/mers.html).

![Case tree plot of MERS clusters](https://github.com/cmrivers/epipy/blob/master/figs/MERS_casetree.png?raw=True)

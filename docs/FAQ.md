Caitlin Rivers (cmrivers@vbi.vt.edu)
Jan 15, 2014

# FAQ
-----
###What is epipy?

Epipy is a python package for epidemiology.  It contains (or will contain...)
tools for analyzing and visualizing epidemiology data.

###What is a case tree plot?

I came up with case tree plots as a way to visualize zoonotic disease.
However, it can also be used to visualizing environmentally-acquired
dieases, or anything that emerges multiple times, is passed from person
to person, and then dies out. Tweets and retweets might be a useful
non-epi example.

###How do I read a case tree plot?

The x axis is time, and the y axis is generation. Nodes along the x axis
are index nodes. In the case of a zoonotic disease, the index node is
a human case acquired from an animal source. If that human were to pass
the disease to two other humans, those two subsequent cases are both
generation 2.

The meaning of the color of the node varies based on the node attribute.
In many cases, color just signifies membership to a human to human
cluster. However, it could also represent health status (e.g. alive, dead),
the sex of the patient, etc. 

###What is a checkerboard plot?

Checkerboard plots display similar data as a case tree plot, but instead
of a network it shows a simple time series for each human to human cluster.
The number in the center of each check is the case id that corresponds
to the the line listing.

###I have a question/complaint/compliment.

Contact me at cmrivers@vbi.vt.edu, or @cmyeaton. Feel free to contribute!

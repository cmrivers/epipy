---
layout: post
category : analyses
tagline: "Basic epidemiology"
tags : [analyses]
---
{% include JB/setup %}


##Summary statistics

The summary() function will return summary statistics if the column contains
numeric values, and the count and frequency of top 5 most common values if the column
contains non-numeric values. Summary can be used either on a single column, or on
a whole dataframe.

It can also return stratified summary statistics using the by argument.

    import epipy as epi
    import pandas as pd

    df = pd.DataFrame({'Age' : [10, 12, 14], 'Group' : ['A', 'B', 'B'] })
    summary(df.Age)

returns:

        count       3
        missing     0
        min        10
        median     12
        mean       12
        std         2
        max        14
        dtype: float64

and:

    summary(df.Group)

returns:

       count      freq
    B      2  0.666667
    A      1  0.333333

finally:

    summary(df.Age, by=df.Group)

returns:

       count  missing  min  median  mean      std   max
    A      1        0   10      10    10       NaN   10
    B      2        0   12      13    13  1.414214   14

              

##2x2 table

###Create a 2x2 table

###Analyze a 2x2 table

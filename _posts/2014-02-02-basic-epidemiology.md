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
    epi.summary(df.Age)

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

    epi.summary(df.Group)

returns:

       count      freq
    B      2  0.666667
    A      1  0.333333

finally:

    epi.summary(df.Age, by=df.Group)

returns:

       count  missing  min  median  mean      std   max
    A      1        0   10      10    10       NaN   10
    B      2        0   12      13    13  1.414214   14

              

##2x2 table

[2x2 tables](http://sphweb.bumc.bu.edu/otlt/MPH-Modules/EP/EP713_Association/EP713_Association_print.html)
are commonly used to assess risk in epidemiology. The rows represent a risk factor,
like exposure to a disease, or sex. The columns represent an outcome, like infection status,
 or whether the disease was severe or mild. 

###Create a 2x2 table

Both rows and columns must be binary, so in the example below I collapse
the health status values into dead and alive. Note that you must tell epipy
how you wish the table to be organized by providing a list of values.

    import epipy as epi
    import pandas as pd

    mers_df = pd.read_csv('epipy/data/mers_line_list.csv')
    mers_df['condensed_health'] = mers_df['Health status'].
                                    replace(['Critical', 'Alive', 'Asymptomatic',
                                    'Mild', 'Recovered', 'Reocvered'], 'Alive')
    table = epi.create_2x2(mers_df, 'Sex', 'condensed_health',
                    ['M', 'F'], ['Dead', 'Alive'])

table returns:

         Dead  Alive  All
    M      46     54  101
    F      16     44   60
    All    70    114  185
    

###Analyze a 2x2 table

2x2 tables are used to calculate odds ratios, relative risk, and chi square tests.

    epi.analyze_2x2(table)

returns:

    Odds ratio: 2.34 (95% CI: (1.17, 4.69))
    Relative risk: 1.73 (95% CI: (1.08, 2.76))

    Chi square: 5.95216712234
    p value: 0.202749053116

Alternatively, you can call each function separately:

    epi.odds_ratio(table)
    epi.relative_risk(table)
    epi.chi2(table)



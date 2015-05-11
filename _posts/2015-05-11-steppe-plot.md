---
layout: post
category : plots
tagline: "Steppe plot"
tags : [plot]
---
{% include JB/setup %}

#Steppe plot

Steppe plots show the interval between two dates for each case in a line list. Common examples include the time betweet onset and death, or onset and report. The steppe plot function works best when NaNs or NaTs are removed.

    import epipy
    import pandas as pd

    df = epipy.get_data('mers_line_list')
    df['death_date'] = df['Approx death date'].apply(epipy.date_convert)
    df = df.dropna(how='any', subset=['onset_date', 'death_date'])
    df = df.tail(15) #select out last 15 cases

    fig, ax = epipy.stripe_plot(df, 'Case #', 'onset_date', 'death_date', 'Sex', legend=True)
    ax.set_ylabel('Case number')
    ax.set_title('Onset to death range (MERS-CoV)')

The result is a nice visualization of the individual case histories across time.

![Steppe plot of selected MERS-CoV cases](http://github.com/cmrivers/epipy/blob/master/figs/steppe_example.png?raw=true)

[Back to documentation](http://cmrivers.github.io/epipy/categories.html)

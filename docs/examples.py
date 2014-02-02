#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
  '''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import epipy
import os

try:
    from mpltools import style, layout
    style.use('ggplot')
    layout.use('ggplot')
except:
    pass

dir = os.path.dirname(__file__)

#################################
# TEST DATA EXAMPLE #
#################################

# Generate example data
example_df = epipy.generate_example_data(cluster_size=7, outbreak_len=180, clusters=7,
                                         gen_time=4, attribute='health')
example_df.to_csv(os.path.join(dir, '../data/example_data.csv'))

# Case tree plot                                        
fig, ax = epipy.case_tree_plot(example_df, cluster_id = 'Cluster', case_id ='ID', date_col='Date', color='Cluster', gen_mean=4, gen_sd = 1)
ax.set_title('Example outbreak data')
fig.savefig(os.path.join(dir, '../figs/example_casetree.png'), bbox_inches='tight')

# Checkerboard plot
fig, ax = epipy.checkerboard_plot(example_df, 'ID', 'Cluster', 'Date')
ax.set_title("Example outbreak data")
fig.savefig(os.path.join(dir, '../figs/test_checkerboard.png'), bbox_inches='tight')


############################
## MERS-CoV DATA EXAMPLE ###
############################

mers_df = pd.read_csv(os.path.join(dir, '../data/mers_line_list.csv'))

# Data cleaning
mers_df['onset_date'] = mers_df['Approx onset date'].map(epipy.date_convert)
mers_df['report_date'] = mers_df['Approx reporting date'].map(epipy.date_convert)
mers_df['dates'] = mers_df['onset_date'].combine_first(mers_df['report_date'])

# Case tree plot
fig, ax = epipy.case_tree_plot(mers_df, cluster_id='Cluster ID', \
                        case_id='Case #', date_col='dates', gen_mean = 5, \
                        gen_sd = 4, color='Cluster ID')
ax.set_title('Human clusters of MERS-CoV')
fig.savefig(os.path.join(dir, '../figs/mers_casetree.png'), bbox_inches='tight')

# Checkerboard plot
fig, ax = epipy.checkerboard_plot(mers_df, 'Case #', 'Cluster ID', 'dates')
ax.set_title("Human clusters of MERS-CoV")
fig.savefig(os.path.join(dir, '../figs/mers_checkerboard.png'), bbox_inches='tight')

#################
### EPICURVES ###
#################

# Daily epicurve of MERS
plt.figure()
epipy.epicurve_plot(mers_df, date_col='dates', freq='day')
plt.title('Approximate onset or report date');
plt.savefig(os.path.join(dir, '../figs/day_epicurve.png'))

# Yearly epicurve of MERS
plt.figure()
epipy.epicurve_plot(mers_df, 'dates', freq='y')
plt.title('Approximate onset or report date')
plt.savefig(os.path.join(dir, '../figs/year_epicurve.png'))

# Monthly epicurve of MERS
plt.figure()
epipy.epicurve_plot(mers_df, 'dates', freq='month')
plt.title('Approximate onset or report date of MERS cases')
plt.savefig(os.path.join(dir, '../figs/month_epicurve.png'))

#################
### ANALYSES ####
#################

# We'll use the MERS data we worked with above
# For this we'll need to build out the graph
mers_G = epipy.build_graph(mers_df, cluster_id='Cluster ID', case_id='Case #',
		date_col='dates', color='Health status', gen_mean=5, gen_sd=4)

# Analyze attribute by generation
fig, ax, table = epipy.generation_analysis(mers_G, attribute='Health status', plot=True)
fig.savefig(os.path.join(dir, '../figs/mers_generation_hist.png'))

# Basic reproduction numbers
R, fig, ax = epipy.reproduction_number(mers_G, index_cases=True, plot=True)
fig.savefig(os.path.join(dir, '../figs/mers_r0_hist.png'))
print 'R0 median: {}'.format(R.median()) # the series object returned can be manipulated further

#2X2 table
mers_df['condensed_health'] = mers_df['Health status'].replace(['Critical', 'Alive', 'Asymptomatic', 'Mild', 'Recovered', 'Reocvered'], 'Alive')
table = epipy.create_2x2(mers_df, 'Sex', 'condensed_health', ['M', 'F'], ['Dead', 'Alive'])
epipy.analyze_2x2(table)

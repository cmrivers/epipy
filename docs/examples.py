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
# GENERATE AN EXAMPLE LINE LIST #
#################################

example_df = epipy.generate_example_data(cluster_size=6, outbreak_len=180, clusters=8,
                                         gen_time=5, attribute='health')
test_clusters = epipy.cluster_builder(example_df, 'Cluster', 'ID', 'Date', 'health', 5, 1)
test_G = epipy.build_graph(test_clusters, color='health')
fig, ax = epipy.case_tree_plot(test_G, color='health')
ax.set_title('Example outbreak data')
ax.set_ylabel('Generations')
ax.grid(True)
fig.savefig(os.path.join(dir, '../figs/example_casetree.png'), bbox_inches='tight')


############################
#### TEST DATA EXAMPLE #####
############################

# if you have in data to load instead of generating it
try:
    test_df = pd.read_pickle(os.path.join(dir, '../data/test_cluster.pkl'))
except:
    from data_generator import generate_example_data
    test_df = generate_example_data(cluster_size=5, outbreak_len=180,
                clusters=10, gen_time=5, attribute='health')
    test_df.to_pickle(os.path.join(dir, '../data/test_cluster.pkl'))

test_clusters = epipy.cluster_builder(test_df, 'Cluster', 'ID', 'Date', 'Cluster', 5, 1)

# Case tree plot
test_G = epipy.build_graph(test_clusters, color='Cluster')
fig, ax = epipy.case_tree_plot(test_G, color='Cluster')
ax.set_title('Example outbreak data')
ax.set_ylabel('Generations')
ax.grid(True)
fig.savefig(os.path.join(dir, '../figs/test_casetree.png'), bbox_inches='tight')

# Checkerboard plot
fig, ax = epipy.checkerboard_plot(test_df, 'ID', 'Cluster', 'Date')
ax.set_title("Test data")
fig.savefig(os.path.join(dir, '../figs/test_checkerboard.png'), bbox_inches='tight')


############################
## MERS-CoV DATA EXAMPLE ###
############################

mers_df = pd.read_csv(os.path.join(dir, '../data/mers_line_list.csv'))

# Data cleaning
mers_df['onset_date'] = mers_df['Approx onset date'].map(epipy.date_convert)
mers_df['report_date'] = mers_df['Approx reporting date'].map(epipy.date_convert)
mers_df['dates'] = mers_df['onset_date'].combine_first(mers_df['report_date'])

# Prepares case clusters for case tree plot
mers_clusters = epipy.cluster_builder(mers_df, 'Cluster ID', 'Case #',
		'dates', 'Cluster ID', 8, 4)

# Case tree plot
mers_G = epipy.build_graph(mers_clusters, color='Cluster ID')
fig, ax = epipy.case_tree_plot(mers_G, color='Cluster ID', loc='upper left')
ax.set_title('Example outbreak data')
ax.grid(True)
fig.savefig(os.path.join(dir, '../figs/mers_casetree.png'), bbox_inches='tight')

# Checkerboard plot
fig, ax = epipy.checkerboard_plot(mers_df, 'Case #', 'Cluster ID', 'dates')
ax.set_title("MERS-CoV clusters")
fig.savefig(os.path.join(dir, '../figs/mers_checkerboard.png'), bbox_inches='tight')

#################
### EPICURVES ###
#################

epi = pd.read_csv(os.path.join(dir, "../data/mers_line_list.csv"), parse_dates=True)

# Data cleaning again
epi['onset_date'] = epi['Approx onset date'].map(lambda x: epipy.date_convert(x, '%Y-%m-%d'))
epi['report_date'] = epi['Approx reporting date'].map(lambda x: epipy.date_convert(x, '%Y-%m-%d'))
epi['dates'] = epi['onset_date'].combine_first(epi['report_date'])

# Daily epicurve
plt.figure()
epipy.epicurve_plot(epi, date_col='dates', freq='day')
plt.title('Approximate onset or report date');
plt.savefig(os.path.join(dir, '../figs/day_epicurve.png'))

# Yearly epicurve
plt.figure()
epipy.epicurve_plot(epi, 'dates', freq='y')
plt.title('Approximate onset or report date')
plt.savefig(os.path.join(dir, '../figs/year_epicurve.png'))

# Monthly epicurve
plt.figure()
epipy.epicurve_plot(epi, 'dates', freq='month')
plt.title('Approximate onset or report date')
plt.savefig(os.path.join(dir, '../figs/month_epicurve.png'))

#################
### ANALYSES ####
#################

# Generate example data
example_df = epipy.generate_example_data(cluster_size=6, outbreak_len=180, clusters=8,
                                         gen_time=5, attribute='health')
test_clusters = epipy.cluster_builder(example_df, 'Cluster', 'ID', 'Date', 'health', 5, 1)
test_G = epipy.build_graph(test_clusters, color='health')

# Analyze attribute by generation
fig, ax = epipy.generation_analysis(test_G, attribute='health', plot=False)
fig.savefig(os.path.join(dir, '../figs/generation_hist.png'))

# Basic reproduction numbers
fig, ax, R = epipy.reproduction_number(test_G, index_cases=True, plot=True)
fig.savefig(os.path.join(dir, '../figs/r0_hist.png'))
print 'R0 median: {}'.format(R.median()) # the series object returned can be manipulated further

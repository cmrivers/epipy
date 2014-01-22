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

example_df = epipy.generate_example_data(cluster_size=6, outbreak_len=90, clusters=5,
                                         gen_time=5, attribute='health')

test_clusters = epipy.cluster_builder(example_df, 'Cluster', 'ID', 'Date', 'Cluster', 5, 1)
test_G = epipy.build_graph(test_clusters)
fig, ax = epipy.case_tree_plot(test_G,  node_size=100)
ax.set_title('Example outbreak data')
ax.set_ylabel('Generations')
ax.grid(True)
fig.savefig(os.path.join(dir, '../figs/test_casetree.png'), bbox_inches='tight')


#####################
# TEST DATA EXAMPLE #
#####################

# load in example data
try:
    test_df = pd.read_pickle(os.path.join(dir, '../data/test_cluster.pkl'))
except:
    from data_generator import generate_example_data
    test_df = generate_example_data(cluster_size=5, outbreak_len=100, clusters=10, generation_time=5)
    test_df.to_pickle(os.path.join(dir, '../data/test_cluster.pkl'))

test_clusters = epipy.cluster_builder(test_df, 'Cluster', 'ID', 'Date', 'Cluster', 5, 1)

# Case tree plot
test_G = epipy.build_graph(test_clusters)
fig, ax = epipy.case_tree_plot(test_G,  node_size=100)
ax.set_title('Example outbreak data')
ax.set_ylabel('Generations')
ax.grid(True)
#fig.savefig(os.path.join(dir, '../figs/test_casetree.png'), bbox_inches='tight')

# Checkerboard plot
fig, ax = epipy.checkerboard_plot(test_df, 'ID', 'Cluster', 'Date')
ax.set_title("Test data")
fig.savefig(os.path.join(dir, '../figs/test_checkerboard.png'), bbox_inches='tight')


#########################
# MERS-CoV DATA EXAMPLE #
#########################

mers_df = pd.read_csv(os.path.join(dir, '../data/mers_line_list.csv'))

# Data cleaning
mers_df['Case #'] = mers_df['Case #'].replace(np.nan, 'single')
mers_df['onset_date'] = mers_df['Approx onset date'].map(epipy.date_convert)
mers_df['report_date'] = mers_df['Approx reporting date'].map(epipy.date_convert)
mers_df['dates'] = mers_df['onset_date'].combine_first(mers_df['report_date'])

# Prepares case clusters for case tree plot
mers_clusters = epipy.cluster_builder(mers_df, 'Cluster ID', 'Case #',
		'dates', 'Cluster ID', 8, 4)

# Case tree plot
mers_G = epipy.build_graph(mers_clusters)
fig, ax = epipy.case_tree_plot(mers_G, node_size=100, loc='upper left')
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

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


#################################
# TEST DATA EXAMPLE #
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
    test_df = pd.read_pickle(os.path.join(dir, 'test_cluster.pkl'))
except:
    test_df = epipy.generate_example_data(cluster_size=7, outbreak_len=120,
                clusters=8, gen_time=7, attribute='sex')
    test_df.to_pickle(os.path.join(dir, '../data/test_cluster.pkl'))

test_clusters = epipy.cluster_builder(test_df, 'Cluster', 'ID', 'Date', 'sex', 3, 1)

# Case tree plot
test_G = epipy.build_graph(test_clusters, color='sex')
fig, ax = epipy.case_tree_plot(test_G, color='sex')
#ax.set_title('Case tree plot using example outbreak data')
ax.set_ylabel('Generations')
ax.grid(True)
fig.savefig(os.path.join(dir, '../figs/test_casetree.png'), bbox_inches='tight')

# Checkerboard plot
fig, ax = epipy.checkerboard_plot(test_df, 'ID', 'Cluster', 'Date')
#ax.set_title("Checkerboard plot using example outbreak data")
fig.savefig(os.path.join(dir, '../figs/test_checkerboard.png'), bbox_inches='tight')
=======
# Generate example data
example_df = epipy.generate_example_data(cluster_size=7, outbreak_len=180, clusters=7, gen_time=4, attribute='health')

# Case tree plot                                        
fig, ax = epipy.case_tree_plot(example_df, cluster_id = 'Cluster', \
                    case_id ='ID', date_col='Date', color='health', \
                    gen_mean=4, gen_sd = 1)
ax.set_title('Example outbreak data')

# Checkerboard plot
fig, ax = epipy.checkerboard_plot(example_df, 'ID', 'Cluster', 'Date')
ax.set_title("Example outbreak data")
>>>>>>> 5d2bbda6261c4906520592480226022cc4e6d357


############################
## MERS-CoV DATA EXAMPLE ###
############################

mers_df = epipy.get_data('mers_line_list')
#you can also get synthetic data using epipy.get_data('example_data')

# Data cleaning
mers_df['onset_date'] = mers_df['Approx onset date'].map(epipy.date_convert)
mers_df['report_date'] = mers_df['Approx reporting date'].map(epipy.date_convert)
mers_df['dates'] = mers_df['onset_date'].combine_first(mers_df['report_date'])

# Case tree plot
fig, ax = epi.case_tree_plot(mers_df, cluster_id='Cluster ID', \
                        case_id='Case #', date_col='dates', gen_mean = 5, \
                        gen_sd = 4, color='condensed_health')
ax.set_title('Human clusters of MERS-CoV')

# Checkerboard plot
fig, ax = epipy.checkerboard_plot(mers_df, 'Case #', 'Cluster ID', 'dates')
ax.set_title("Human clusters of MERS-CoV")

#################
### EPICURVES ###
#################

# Daily epicurve of MERS
plt.figure()
curve, fig, ax = epipy.epicurve_plot(mers_df, date_col='dates', freq='day')
plt.title('Approximate onset or report date');

# Yearly epicurve of MERS
plt.figure()
epipy.epicurve_plot(mers_df, 'dates', freq='y')
plt.title('Approximate onset or report date')

# Monthly epicurve of MERS
plt.figure()
curve, fig, ax = epipy.epicurve_plot(mers_df, 'dates', freq='month')
plt.title('Approximate onset or report date of MERS cases')

#################
### ANALYSES ####
#################

# We'll use the MERS data we worked with above
# For this we'll need to build out the graph
mers_G = epipy.build_graph(mers_df, cluster_id='Cluster ID', case_id='Case #',
		date_col='dates', color='Health status', gen_mean=5, gen_sd=4)

# Analyze attribute by generation
fig, ax, table = epipy.generation_analysis(mers_G, attribute='Health status', plot=True)


# Basic reproduction numbers
R, fig, ax = epipy.reproduction_number(mers_G, index_cases=True, plot=True)
print 'R0 median: {}'.format(R.median()) # the series object returned can be manipulated further

#2X2 table
mers_df['condensed_health'] = mers_df['Health status'].replace(['Critical', 'Alive', 'Asymptomatic', 'Mild', 'Recovered', 'Reocvered'], 'Alive')
table = epipy.create_2x2(mers_df, 'Sex', 'condensed_health', ['M', 'F'], ['Dead', 'Alive'])
epipy.analyze_2x2(table)

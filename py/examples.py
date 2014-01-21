# -*- coding: utf-8 -*-
'''
  -------------
 * Caitlin Rivers
 * [cmrivers@vbi.vt.edu](cmrivers@vbi.vt.edu)
  -------------
  '''
import pandas as pd
import epipy
import matplotlib.pyplot as plt

try:
    from mpltools import style, layout
    style.use('ggplot')
    layout.use('ggplot')
except:
    pass

#####################
# TEST DATA EXAMPLE #
#####################
test_df = pd.read_pickle('../data/test_network.pkl')
test_clusters = epipy.cluster_builder(test_df, 'Cluster', 'ID', 'Date', 'Cluster', 5, 1)

# Case tree plot
test_G = epipy.build_graph(test_clusters)
fig, ax = epipy.plotting(test_G,  node_size=100)
ax.set_title('Example outbreak data')
ax.set_ylabel('Generations')
ax.grid(True)
fig.savefig('../figs/test_casetree.png', bbox_inches='tight')

# Checkerboard plot
fig, ax = epipy.plot_cluster(test_df, 'ID', 'Cluster', 'Date')
ax.set_title("Test data")
fig.savefig('../figs/test_checkerboard.png')


#########################
# MERS-CoV DATA EXAMPLE #
#########################

mers_df = pd.read_csv('../data/mers_line_list.csv')

# Data cleaning
mers_df['Case #'] = mers_df['Case #'].replace(np.nan, 'single')
mers_df['onset_date'] = mers_df['Approx onset date'].map(epipy.date_convert)
mers_df['report_date'] = mers_df['Approx reporting date'].map(epipy.date_convert)
mers_df['dates'] = mers_df['onset_date'].combine_first(dat['report_date']) 

# Prepares case clusters for case tree plot
mers_clusters = epipy.cluster_builder(mers_df, 'Cluster ID', 'Case #',
		'dates', 'Cluster ID', 8, 4)

# Case tree plot
mers_G = epipy.build_graph(mers_clusters)
fig, ax = epipy.plotting(mers_G,  node_size=100)
ax.set_title('Example outbreak data')
ax.set_ylabel('Generations')
ax.grid(True)
fig.savefig('../figs/mers_casetree.png', bbox_inches='tight')

# Checkerboard plot
fig, ax = plot_cluster(mers_df, clusters, 'Case #', 'Cluster ID', 'dates')
ax.set_title("MERS-CoV clusters")
fig.savefig('../figs/mers_checkerboard.png')

#################
### EPICURVES ###
#################

epi = pd.read_csv("../data/mers_line_list", parse_dates=True)

# Data cleaning again
epi['onset_date'] = epi['Approx onset date'].map(lambda x: epipy.date_convert(x, '%Y-%m-%d'))
epi['report_date'] = epi['Approx reporting date'].map(lambda x: epipy.date_convert(x, '%Y-%m-%d'))
epi['dates'] = epi['onset_date'].combine_first(epi['report_date']) 

# Daily epicurve
epipy.epicurve(epi, date_col='dates', freq='day')
plt.title('Approximate onset or report date');
plt.savefig('../figs/day_epicurve.png')

# Yearly epicurve
epipy.epicurve(epi, 'dates', freq='y')
plt.title('Approximate onset or report date')
plt.savefig('../figs/year_epicurve.png');

# Monthly epicurve
epipy.epicurve(epi, 'dates', freq='month')
plt.title('Approximate onset or report date')
plt.savefig('../figs/month_epicurve.png')

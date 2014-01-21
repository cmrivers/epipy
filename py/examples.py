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
except:
    pass



#def main(fpath, cluster_id, case_id, dates, colors, gen_mean, gen_sd, save=None):
    
    #if fpath.split('.')[-1] == '.csv':
	#df = pd.read_csv(fpath, parse_dates=True)
    #elif fpath.split('.')[-1] == 'pkl':
	#df = pd.read_pickle(fpath)
    #else:
	#print 'File not recognized'
	
    #df[case_id] = df[case_id].replace(np.nan, 'single')
    #clusters = cluster_builder(df, cluster_id, case_id, dates, gen_mean, gen_sd)

    #if save != None:
	#clusters.to_pickle(save)

    #return clusters


#clusters = main('test_cluster.pkl', 'Cluster', 'ID', 'Date', 'Cluster', 5, 1, '../data/test_network.pkl')
#fig, ax = plot_cluster(dat, clusters, 'ID', 'Cluster', 'Date')
#ax.set_title("Test data")
#fig.savefig('../figs/test_clusters.png')



#dat['onset_date'] = dat['Approx onset date'].map(date_convert)
#dat['report_date'] = dat['Approx reporting date'].map(date_convert)
#dat['dates'] = dat['onset_date'].combine_first(dat['report_date']) #combines onset and report date columns, with onset date preferential

#fig, ax = plot_cluster(dat, clusters, 'Case #', 'Cluster ID', 'dates')
#ax.set_title("MERS-CoV clusters")
#fig.savefig('../figs/cluster_checkerboard.png')

#def example_data(dataset='test_cluster'):
    #epi = pd.read_pickle('../data/{}.pkl'.format(dataset))
    #epi.time = pd.to_datetime(epi.time)
    #epi[['case_id', 'source_node', 'index_node']] = epi[['case_id', 'source_node', 'index_node']].astype('int')
    #epi['pltdate'] = [mpl.dates.date2num(i) for i in epi.time]



    ##dat = pd.read_pickle('test_cluster.pkl')



#df = example_data(dataset='test_network')
#G = build_graph(df, color='color', case_id='case_id', source='source_node', index='index_node', date='pltdate')

#fig, ax = plotting(G,  node_size=100)
#ax.set_title('Example outbreak data')
#ax.set_ylabel('Generations')
#ax.grid(True)
##fig.savefig('../figs/casetree.png', bbox_inches='tight')
#fig.savefig('../figs/test_casetree.png', bbox_inches='tight')
#plt.show()

### EPICURVES ###

epi = pd.read_csv("../data/Line list & epi stats - Line list.csv", parse_dates=True)
epi['onset_date'] = epi['Approx onset date'].map(lambda x: epipy.date_convert(x, '%Y-%m-%d'))
epi['report_date'] = epi['Approx reporting date'].map(lambda x: epipy.date_convert(x, '%Y-%m-%d'))
epi['dates'] = epi['onset_date'].combine_first(epi['report_date']) 

epipy.epicurve(epi, date_col='dates', freq='day')
plt.title('Approximate onset or report date');
plt.savefig('../figs/day_epicurve.png')

epipy.epicurve(epi, 'dates', freq='y')
plt.title('Approximate onset or report date')
plt.savefig('../figs/year_epicurve.png');

epipy.epicurve(epi, 'dates', freq='month')
plt.title('Approximate onset or report date')
plt.savefig('../figs/month_epicurve.png')

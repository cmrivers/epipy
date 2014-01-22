# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import itertools
import string


def _date_choice(ix_date, generation_time):
    date_rng = pd.date_range(ix_date, periods=generation_time*2, freq='D')
    date = np.random.choice(date_rng, 1)
    
    return date

def generate_example_data(cluster_size, outbreak_len, clusters, generation_time):
    line_list = []    
    used = []
    for i in range(clusters):
        cluster_name = np.random.choice([i for i in string.letters if i not in used])[0]
        used.append(cluster_name)
        
        ix_rng = pd.date_range('1/1/2014', periods=outbreak_len, freq='D')
        ix_date = np.random.choice(ix_rng, size=1)
        
        rng = int(np.random.normal(cluster_size, 2, 1))
        for n in range(rng):
            date = _date_choice(ix_date[0], generation_time*2)[0]            
            sex =  np.random.choice(['M', 'F'], size=1)[0]
            line_list.append((len(line_list), date, cluster_name, sex))

    return pd.DataFrame(line_list, columns=['ID', 'Date', 'Cluster', 'Sex'])



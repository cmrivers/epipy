# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from datetime import timedelta, datetime
import itertools
import string


def _date_choice(ix_date, gen_time):
    date_rng = pd.date_range(ix_date, periods=gen_time*2, freq='D')
    date = np.random.choice(date_rng, 1)

    return date


def generate_example_data(cluster_size, outbreak_len, clusters, gen_time, attribute='sex'):
    """
    Generates example outbreak data

    PARAMETERS
    ------------------------------
    cluster_size = mean number of cases in cluster. Build in sd of 2
    outbreak_len = duration of outbreak in days
    clusters = number of clusters to begenerated
    gen_time = time between cases in a cluster
    attribute = case attribute. Options are 'sex' (returns M, F) and
                'health' (returns asymptomatic, alive, critical, dead)

    RETURNS
    ------------------------------
    pandas dataframe with columns ['ID', 'Date', 'Cluster', 'Sex']

    """
    line_list = []
    used = []
    for i in range(clusters):
        cluster_letter = np.random.choice([i for i in string.ascii_uppercase if i not in used])[0]
        cluster_name = 'Cluster' + cluster_letter
        used.append(cluster_letter)

        ix_rng = pd.date_range('1/1/2014', periods=outbreak_len, freq='D')
        ix_date = np.random.choice(ix_rng, size=1)

        rng = int(np.random.normal(cluster_size, 1, 1))
        if rng < 2:
            rng += 1

        for n in range(rng):
            date = _date_choice(ix_date[0], gen_time)[0]

            if attribute.lower() == 'sex':
                attr =  np.random.choice(['Male', 'Female'], size=1)[0]
            elif attribute.lower() == 'health':
                attr = np.random.choice(['asymptomatic', 'alive', 'critical', 'dead'], size=1)[0]

            line_list.append((len(line_list), date, cluster_name, attr))

    return pd.DataFrame(line_list, columns=['ID', 'Date', 'Cluster', attribute])

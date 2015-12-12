#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import pandas as pd
import string


def _date_choice(ix_date, gen_time):
    date_rng = pd.date_range(ix_date, periods=gen_time*2, freq='D')
    date = np.random.choice(date_rng, 1)

    return date


def generate_example_data(cluster_size, outbreak_len, clusters, gen_time):
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
    pandas dataframe with columns ['caseid', 'date', 'cluster', 'sex', 'health', 'exposure']

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

        dates = [ix_date[0]]
        for n in range(rng):
            date = _date_choice(dates[-1], gen_time)[0]
            dates.append(date)

            attr1 =  np.random.choice(['Male', 'Female'], size=1)[0]
            attr2 = np.random.choice(['asymptomatic', 'alive', 'critical', 'dead'], size=1)[0]
            attr3 = np.random.choice(['exposed', 'notexposed'], size=1)[0]

            line_list.append((len(line_list), date, cluster_name, attr1, attr2, attr3))

    return pd.DataFrame(line_list, columns=['caseid', 'date', 'cluster', 'sex', 'health', 'exposure'])

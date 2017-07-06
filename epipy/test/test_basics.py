#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pytest
import basics

def _test_data():
    _data = [(0, 'ClusterA', '2013-01-01', 'M'),
            (1, 'ClusterB', '2013-01-01', 'F'),
            (2, 'ClusterA', np.nan, 'M'),
            (3, 'ClusterC', '2013-01-04', 'F'),
            (4, 'ClusterB', '2013-01-03', 'M'),
            (5, 'ClusterB', '2013-01-05', 'M')]
    df = pd.DataFrame(_data, columns=['id', 'cluster', 'date', 'sex'])

    return df


def test_date_convert_str():
    df = _test_data()
    str_val = df.date[0]
    dtime = basics.date_convert(str_val)

    assert type(dtime) == datetime
    assert dtime == datetime.date(2013, 1, 1)


def test_date_convert_nan():
    df = _test_data()
    nan_val = df.date[2]
    dtime = basics.date_convert(nan_val)
    
    assert type(dtime) == float
    assert np.isnan(dtime) == True


def test_date_convert_wrongformat():
    wrong_val = '01-2012-01'

    with pytest.raises(ValueError):
        dtime = basics.date_convert(wrong_val)


def test_date_convert_wrongformat2():
    wrong_int = 1201201

    with pytest.raises(ValueError):
        dtime = basics.date_convert(wrong_int)

    
def test_group_clusters():
    df = _test_data()
    groups = basics.group_clusters(df, 'cluster', 'date')

    assert len(groups) == 3
    assert groups.groups == {'ClusterA': [0], 'ClusterB': [1, 4, 5], \
                            'ClusterC': [3]}


def test_cluster_to_tuple():
    df = _test_data()
    df['datetime'] = df['date'].map(basics.date_convert)

    df_out = basics.cluster_builder(df, 'cluster', 'id', 'datetime', \
                                    'sex', 2, 1)
    df_out = df_out.sort('case_id')

    #sanity check
    assert df_out.ix[0]['case_id'] == 0
    assert df_out.ix[3]['case_id'] == 3
    #index nodes
    assert df_out.ix[0]['index_node'] == 0
    assert df_out.ix[4]['index_node'] == 1
    #source nodes
    assert df_out.ix[5]['source_node'] == 4

    

    

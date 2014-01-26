#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import datetime
import pytest
import basics

def _test_data():
    _data = [(0, 'ClusterA', '2013-01-01', 'M'),
            (1, 'ClusterB', '2013-01-01', 'F'),
            (2, 'ClusterA', np.nan, 'M'),
            (3, 'ClusterC', '2013-01-01', 'F'),
            (4, 'ClusterB', '2013-01-01', 'M')]
    df = pd.DataFrame(_data, columns=['id', 'cluster', 'date', 'sex'])

    return df


def test_date_convert_str():
    df = _test_data()
    str_val = df.date[0]
    dtime = basics.date_convert(str_val)

    assert type(dtime) == datetime
    assert dtime == datetime(2013, 01, 01)


def test_date_convert_nan():
    df = _test_data()
    nan_val = df.date[2]
    dtimenan = basics.date_convert(nan_val)
    
    assert type(dtimenan) == float
    assert np.isnan(dtimenan) == True

    
def test_group_clusters():
    df = _test_data()
    groups = basics.group_clusters(df, 'cluster', 'date')

    assert len(groups) == 3
    assert groups.groups == {'ClusterA': [0], 'ClusterB': [1, 4], \
                            'ClusterC': [3]}


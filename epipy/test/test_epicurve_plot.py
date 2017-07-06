#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from random import sample
import epicurve

def _test_data():
    times = pd.date_range('12/1/2013', periods=60, freq='d')
    times = times.to_datetime()
    _data = [(0, 'ClusterA',  0, 0),
            (1, 'ClusterB', 1, 1),
            (2, 'ClusterA', 0, 0),
            (3, 'ClusterA', 0, 2),
            (4, 'ClusterB', 1, 1),
            (5, 'ClusterB', 1, 4)]
    df = pd.DataFrame(_data, columns=['case_id', 'cluster', 'index_node', 'source_node'])
    df['pltdate'] = sample(times, len(_data))
    
    return df
    

def test_epicurve_plot_month():
    data = _test_data()
    curve, fig, ax = epicurve.epicurve_plot(data, 'pltdate', 'm')
    
    assert len(curve) == 2
    assert curve['count'].sum() == 6


def test_epicurve_plot_day():
    data = _test_data()
    curve, fig, ax = epicurve.epicurve_plot(data, 'pltdate', 'd')
    
    assert len(curve) == 6
    assert curve['count'].sum() == 6


def test_epicurve_plot_year():
    data = _test_data()
    curve, fig, ax = epicurve.epicurve_plot(data, 'pltdate', 'y')
    
    assert len(curve) == 2
    assert curve['count'].sum() == 6
    
    




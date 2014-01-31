#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pytest
import case_tree

def _test_data():
    times = pd.date_range('1/1/2013', periods=6, freq='d')
    times = times.to_datetime()
    _data = [(0, 'ClusterA',  0, 0),
            (1, 'ClusterB', 1, 1),
            (2, 'ClusterA', 0, 0),
            (3, 'ClusterA', 0, 2),
            (4, 'ClusterB', 1, 1),
            (5, 'ClusterB', 1, 4)]
    df = pd.DataFrame(_data, columns=['case_id', 'cluster', 'index_node', 'source_node'])
    df['pltdate'] = times
    
    return df


def test_build_graph_graph():
    data = _test_data()
    G = case_tree.build_graph(data, 'cluster')

    assert len(G.node) == 6
    edges = [(0, 0), (1, 1), (0, 2), (2, 3), (1, 4), (4, 5)]
    assert len(G.edges()) == len(edges)
    for tup in G.edges():
        assert tup in edges


def test_build_graph_generation():
    data = _test_data()
    G = case_tree.build_graph(data, color='cluster')
    assert G.node[0]['generation'] == 0
    assert G.node[1]['generation'] == 0
    assert G.node[2]['generation'] == 1
    assert G.node[3]['generation'] == 2
    assert G.node[4]['generation'] == 1
    assert G.node[5]['generation'] == 2
    




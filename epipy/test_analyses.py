#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import pandas as pd
import networkx as nx
import pytest
import analyses

def test_ordered_table_list():
    table = [(0, 1),
             (2, 3)]

    a, b, c, d = analyses._ordered_table(table)
    assert a == 0
    assert b == 1
    assert c == 2
    assert d == 3


def test_ordered_table_numpy():
    table = [(0, 1),
             (2, 3)]
    table = np.array(table)

    a, b, c, d = analyses._ordered_table(table)
    assert a == 0
    assert b == 1
    assert c == 2
    assert d == 3


def test_ordered_table_DataFrame():
    table = [(0, 1),
             (2, 3)]
    table = pd.DataFrame(table)
    
    a, b, c, d = analyses._ordered_table(table)
    assert a == 0
    assert b == 1
    assert c == 2
    assert d == 3


def test_ordered_table_typeError():
    table = [(0, 1),
             (2, 3)]
    table = np.matrix(table)

    with pytest.raises(TypeError):
        a, b, c, d = analyses._ordered_table(table)
    

    
def test_odds_ratio():
    table = [(1, 2),
             (3, 4)]

    ratio, or_ci = analyses.odds_ratio(table)

    assert np.allclose(ratio, .6667, atol=.01)
    assert np.allclose(or_ci, (0.03939, 11.28), atol=.01)


def test_relative_risk():
    table = [(1, 2),
             (3, 4)]

    rr, rr_ci = analyses.relative_risk(table)

    assert np.allclose(rr, 0.7778, atol=.01)
    assert np.allclose(rr_ci, (0.1267, 4.774), atol=.01)


def test_chi2():
    table = [(1, 2),
             (3, 4)]

    chi2, p, dof, expected = analyses.chi2(table)

    assert np.allclose(chi2, 0.1786, atol=.01)


def test_AR():
    table = [(1, 2),
             (3, 4)]

    ar, arp, par, parp = analyses.attributable_risk(table)

    assert np.allclose(ar, -.095, atol=.01)
    assert np.allclose(arp, -28.57, atol=.01)
    assert np.allclose(par, -.0386, atol=.01)
    assert np.allclose(parp, -7.143, atol=.01)


def test_create2x2():
    df = pd.DataFrame({'Exposed':['Y', 'Y', 'N', 'Y'], \
                          'Sick':['Y', 'N', 'N', 'Y']})
    table = analyses.create_2x2(df, 'Exposed', 'Sick', ['Y', 'N'], \
            ['Y', 'N'])

    assert table.ix[0][0] == 2
    assert table.ix[0][1] == 1
    assert table.ix[1][0] == 0
    assert table.ix[1][1] == 1


def test_2x2_errorRaises():
    df = pd.DataFrame({'Exposed':['Y', 'Y', 'N', 'Y'], \
                          'Sick':['Y', 'N', 'N', 'Y']})
            
    with pytest.raises(TypeError):
        table = analyses.create_2x2(df, 'Exposed', 'Sick', ['Y', 'N'], \
            'Y')

    with pytest.raises(AssertionError):
        table = analyses.create_2x2(df, 'Exposed', 'Sick', ['Y', 'N'], \
            ['Y'])

def _create_graph():
    G = nx.DiGraph()
    G.add_nodes_from([3, 4, 5])
    G.node[3]['generation'] = 0
    G.node[4]['generation'] = 1
    G.node[5]['generation'] = 1
    G.node[3]['health'] = 'alive'
    G.node[4]['health'] = 'dead'
    G.node[5]['health'] = 'alive'
    G.add_edges_from([(3, 4), (3, 5)])
    
    return G

    
def test_generation_analysis():
    G = _create_graph()
    table = analyses.generation_analysis(G, 'health', plot=False)

    assert table.ix[0][0] == 1
    assert table.ix[0][1] == 0
    assert table.ix[1][0] == 1
    assert table.ix[1][1] == 1

    
def test_reproduction_number_index():
    G = _create_graph()
    R = analyses.reproduction_number(G, index_cases=True, plot=False)

    assert len(R) == 3
    assert R.iget(0) == 2
    assert R.iget(1) == 0
    assert R.iget(2) == 0


def test_reproduction_number_noindex():
    G = _create_graph()
    R = analyses.reproduction_number(G, index_cases=False, plot=False)

    assert len(R) == 2
    assert R.iget(0) == 0
    assert R.iget(1) == 0


def test_numeric_summary():
    df = pd.DataFrame({'Age' : [10, 12, 14], 'Group' : ['A', 'B', 'B'] })
    summ = analyses.summary(df.Age)
    
    assert summ['count'] == 3
    assert summ['missing'] == 0
    assert summ['min'] == 10
    assert summ['median'] == 12
    assert summ['mean'] == 12
    assert summ['std'] == 2
    assert summ['max'] == 14


def test_categorical_summary():
    df = pd.DataFrame({'Age' : [10, 12, 14], 'Group' : ['A', 'B', 'B'] })
    summ = analyses.summary(df.Group)
    
    assert summ.ix[0]['count'] == 2
    assert  np.allclose(summ.ix[0]['freq'], 2/3, atol=.01)


def test_grouped_summary():
    df = pd.DataFrame({'Age' : [10, 12, 14], 'Group' : ['A', 'B', 'B'] })
    summ = analyses.summary(df.Age, df.Group)

    assert len(summ) == 2
    assert len(summ.columns) == 7


       
    

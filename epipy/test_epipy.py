#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import networkx as nx
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


def test_create2x2():
    df = pd.DataFrame({'Exposed':['Y', 'Y', 'N', 'Y'], \
                          'Sick':['Y', 'N', 'N', 'Y']})
    table = analyses.create_2x2(df, 'Exposed', 'Sick', ['Y', 'N'], \
            ['Y', 'N'])

    assert table.ix[0][0] == 2
    assert table.ix[0][1] == 1
    assert table.ix[1][0] == 0
    assert table.ix[1][1] == 1


def test_generation_analysis():
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2])
    G.node[0]['generation'] = 0
    G.node[1]['generation'] = 0
    G.node[2]['generation'] = 1
    G.node[0]['health'] = 'alive'
    G.node[1]['health'] = 'dead'
    G.node[2]['health'] = 'alive'

    table = analyses.generation_analysis(G, 'health', plot=False)

    assert table.ix[0][0] == 1
    assert table.ix[0][1] == 1
    assert table.ix[1][0] == 1
    assert table.ix[1][1] == 0
    


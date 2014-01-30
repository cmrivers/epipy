#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pytest
import data_generator


def test_generate_example_data():
    data = data_generator.generate_example_data(cluster_size=5, outbreak_len=180,
                clusters=10, gen_time=5, attribute='health')
    
    assert np.allclose(len(data), 50, rtol=.1)
    assert len(data.Cluster.unique()) == 10
    

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pytest
import data_generator


def test_generate_example_data():
    data = data_generator.generate_example_data(cluster_size=5, outbreak_len=180,
                clusters=10, gen_time=5, attribute='health')
    
    assert len(data.Cluster.unique()) == 10
    

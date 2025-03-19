#!/usr/bin/env python3

import typing

import pandas as pd

from src.python.soft_sensors import SoftSensor
from src.python.soft_sensors.shc import ShcSoftSensor

def test_shc():
    data = {
        'timestamp': ['2023-01-01 00:00:00'],
        's_ph_sil_tput': [160.0], # mass of raw meal
        'f_k_coal_tput': [12.9], # mass of coal 
        'f_k_coal_ncv': [6000], # net calorific value
    }

    df = pd.DataFrame(data)

    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)

    expected = 749

    assert result.shc[0] == expected


def test_shc_from_file(test_data):
    df = test_data("abc.csv")
    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)

    expected_json = {"2023-01-01 00:00:00": 746, 
                     "2023-01-01 01:00:00": 764,
                     }
    
    for date, expected_shc in expected_json.items():

        actual_shc = result.loc[result['timestamp'] == date, 'shc'].values
        assert actual_shc == expected_shc

if typing.TYPE_CHECKING:
    x: SoftSensor = ShcSoftSensor()

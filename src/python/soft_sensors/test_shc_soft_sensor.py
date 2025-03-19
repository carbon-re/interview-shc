#!/usr/bin/env python3

import typing

import pandas as pd

from src.python.soft_sensors import SoftSensor
from src.python.soft_sensors.shc import ShcSoftSensor

# 
def test_shc():
    data = {
        'timestamp': ['2023-01-01 00:00:00'],
        's_ph_sil_tput': [160.0],  # tonnes / hour (clinker)
        'f_k_coal_tput': [12.9],  # tonnes / hour (coal in kiln)
        'f_k_coal_ncv': [6000],  # net calorific output (coal)
    }

    df = pd.DataFrame(data)

    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)

    expected = 749

    assert result['shc'][0] == expected


def test_shc_from_file(test_data):
    sensor = ShcSoftSensor()

    df = test_data("abc.csv")
    print(df)

    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)

    result = df.loc[df["timestamp"] == "2023-01-01 10:00:00"]['shc'].values

    expected_result = 723
    
    assert result == expected_result

if typing.TYPE_CHECKING:
    x: SoftSensor = ShcSoftSensor()

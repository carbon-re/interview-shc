#!/usr/bin/env python3

import typing

import pandas as pd

from src.python.soft_sensors import SoftSensor
from src.python.soft_sensors.shc import ShcSoftSensor


def test_shc():
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "s_ph_sil_tput": [160.0], # raw meal 
        "f_k_coal_tput": [12.9], # mass of fuel 
        "f_k_coal_ncv": [6000], # net calorific value
        # mass of klinker = 160 / 1.55 mass of klinker = 103
        # heat = 12.9 * 6000 heat generated = 77400
        # shc = 751 
    }

    df = pd.DataFrame(data)

    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)



    assert result.shc[0] == 749


def test_shc_from_file(test_data):
    df = test_data("abc.csv")
    Expected = len(df.index)
    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)

    if Expected != len(result.index):
        assert False
    else:
        assert True
   
def Nan_value():
    data = {
            "timestamp": ["2023-01-01 00:00:00","2023-01-01 16:00:00"],
            "s_ph_sil_tput": [160.0,0.00021064633213745365], # raw meal 
            "f_k_coal_tput": [12.9,14.2680151413933323e-05,], # mass of fuel 
            "f_k_coal_ncv": [5500, None], # net calorific value
            # mass of klinker = 160 / 1.55 mass of klinker = 103
            # heat = 12.9 * 6000 heat generated = 77400
            # shc = 751 
        }
    df = pd.DataFrame(data)

    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)
    assert len(df["f_k_coal_ncv"].notnull) > 1
if typing.TYPE_CHECKING:
    x: SoftSensor = ShcSoftSensor()

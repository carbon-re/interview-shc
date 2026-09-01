#!/usr/bin/env python3

import typing

import pandas as pd

from src.python.soft_sensors import SoftSensor
from src.python.soft_sensors.shc import ShcSoftSensor


def test_shc():
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "s_ph_sil_tput": [160.0], # kilt feed / raw meal
        "f_k_coal_tput": [12.9], # coal fuel input
        "f_k_coal_ncv": [6000], # net caloric value (for coal)
    }

    df = pd.DataFrame(data)

    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)

    # shc = (heat) / (mass of clinker)
    #
    # where mass of clinker = (mass of **raw meal** / **clinker ratio**)
    # and heat = the sum of (mass of fuel * **net calorific value**) for each fuel
    #
    # heat = sum (f_k_coal_tput * f_k_coal_ncv) -> 12.9 * 6000
    # mass of clinker = s_ph_sil_tput / clinker ratio -> 160.0 / 1.55

    assert result.shc[0] == (12.9 * 6000) / (160.0 / 1.55)


def test_shc_from_file(test_data):
    df = test_data("abc.csv")
    print(df)
    assert False


if typing.TYPE_CHECKING:
    x: SoftSensor = ShcSoftSensor()

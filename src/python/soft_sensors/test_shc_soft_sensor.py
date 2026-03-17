#!/usr/bin/env python3

import typing

import pandas as pd

from src.python.soft_sensors import SoftSensor
from src.python.soft_sensors.shc import ShcSoftSensor


def test_shc():
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "s_ph_sil_tput": [160.0],
        "f_k_coal_tput": [12.9],
        "f_k_coal_ncv": [6000],
    }

    df = pd.DataFrame(data)

    sensor = ShcSoftSensor()
    result = sensor.calculate(df)

    expected_heat_consumption = (12.9 * 6000) / (160.0 / 1.55)

    expected = pd.DataFrame(
        {
            "timestamp": ["2023-01-01 00:00:00"],
            "heat_consumption": [expected_heat_consumption],
        }
    )
    print(result)

    assert result == expected


# def test_shc_from_file(test_data):
#     df = test_data("abc.csv")
#     print(df)
#     assert False


if typing.TYPE_CHECKING:
    x: SoftSensor = ShcSoftSensor()

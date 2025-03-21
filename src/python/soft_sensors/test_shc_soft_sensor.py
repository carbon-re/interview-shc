#!/usr/bin/env python3

import typing

import pandas as pd
from pandas.testing import assert_frame_equal

from src.python.soft_sensors import SoftSensor
from src.python.soft_sensors.shc import ShcSoftSensor


def test_transform():
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "s_ph_sil_tput": [160.0],
        "f_k_coal_tput": [12.9],
        "f_k_coal_ncv": [6000],
    }

    df = pd.DataFrame(data)

    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)

    expected_dictionary = {
        "timestamp": ["2023-01-01 00:00:00"],
        "heat": [77400.0],
        "clinker_mass": [103.2258064516129],
    }
    expected_result = pd.DataFrame(expected_dictionary)

    assert_frame_equal(transformed, expected_result)


def test_calculate():
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "heat": [77400.0],
        "clinker_mass": [103.2258064516129],
    }

    df = pd.DataFrame(data)

    sensor = ShcSoftSensor()
    calculated = sensor.calculate(df)

    expected_dictionary = {"timestamp": ["2023-01-01 00:00:00"], "shc": [749]}
    expected_result = pd.DataFrame(expected_dictionary)

    assert_frame_equal(calculated, expected_result)


def test_shc():
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "s_ph_sil_tput": [160.0],
        "f_k_coal_tput": [12.9],
        "f_k_coal_ncv": [6000],
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
    resulting_dataframe = sensor.calculate(transformed)

    expected_dictionary = {
        "timestamp": ["2023-01-01 00:00:00", "2023-01-01 01:00:00"],
        "shc": [746, 764],
    }
    expected_result = pd.DataFrame(expected_dictionary)

    assert_frame_equal(resulting_dataframe.head(2), expected_result)


if typing.TYPE_CHECKING:
    x: SoftSensor = ShcSoftSensor()

#!/usr/bin/env python3

import typing

import pandas as pd

from src.python.soft_sensors import SoftSensor
from src.python.soft_sensors.shc import ShcSoftSensor


def calculate(df: pd.DataFrame) -> pd.DataFrame:
    sensor = ShcSoftSensor()
    return sensor.calculate(sensor.transform(df))


def test_shc():
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "s_ph_sil_tput": [160.0],
        "f_k_coal_tput": [12.9],
        "f_k_coal_ncv": [6000],
    }

    result = calculate(pd.DataFrame(data))

    # 12.9 t/h coal * 1000 * 6000 kcal/kg = 77_400_000 kcal/h of heat,
    # over (160 t/h / 1.55) * 1000 = 103_225.8 kg/h of clinker.
    expected = 749

    assert result.shc.iloc[0] == expected


def test_shc_rounds_down():
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "s_ph_sil_tput": [160.0],
        "f_k_coal_tput": [12.9],
        "f_k_coal_ncv": [6000],
    }

    result = calculate(pd.DataFrame(data))

    # The exact value is 749.81..., which must floor rather than round to 750.
    assert result.shc.iloc[0] == 749


def test_shc_from_file(test_data):
    df = test_data("abc.csv")

    result = calculate(df)

    assert len(result) == len(df)
    assert result.index.is_monotonic_increasing
    assert result.shc.notna().all()
    # A well run plant sits in the high 600s to low 800s kcal/kg.
    assert result.shc.between(600, 900).all()


if typing.TYPE_CHECKING:
    x: SoftSensor = ShcSoftSensor()

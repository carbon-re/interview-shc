#!/usr/bin/env python3


from src.python.soft_sensors.handler import transform
from src.python.soft_sensors.shc import RdfShcSoftSensor, ShcSoftSensor


def test_transform(test_data):
    df = test_data("abc.csv")
    sensor = ShcSoftSensor()
    result = transform(df, sensor)
    assert isinstance(result, dict)
    assert result["2023-01-01 01:00:00"] == 764


def test_using_latest_ncv_value(test_data):
    df = test_data("bcd.csv")
    sensor = ShcSoftSensor()
    result = transform(df, sensor)
    assert isinstance(result, dict)
    assert result["2023-01-01 08:00:00"] == 767
    assert "2023-01-01 16:00:00" not in result


def test_cde(test_data):
    df = test_data("cde.csv")
    sensor = RdfShcSoftSensor()
    result = transform(df, sensor)
    assert isinstance(result, dict)
    assert result["2023-01-01 11:00:00"] == 789
    assert result["2023-01-21 01:00:00"] == 805
    assert result["2023-01-25 14:00:00"] == 794


def test_def(test_data):
    df = test_data("def.csv")
    sensor = RdfShcSoftSensor()
    result = transform(df, sensor)
    assert isinstance(result, dict)
    assert result["2025-01-01 02:00:00"] == 811

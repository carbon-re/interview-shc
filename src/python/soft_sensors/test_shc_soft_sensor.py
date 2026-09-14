#!/usr/bin/env python3

import pandas as pd

from src.python.soft_sensors.shc import calculate, transform


def test_shc_success() -> None:
    """Test that the shc calculation works correctly."""
    data = {
        "timestamp": ["2023-01-01 00:00:00"],
        "s_ph_sil_tput": [160.0],
        "f_k_coal_tput": [12.9],
        "f_k_coal_ncv": [6000],
    }

    df = pd.DataFrame(data)

    transformed = transform(df)
    result = calculate(transformed)

    assert isinstance(result, pd.DataFrame)
    assert result["shc"][0] == 749.8125


def test_shc_from_file(test_data) -> None:
    df = test_data("abc.csv")
    assert isinstance(df, pd.DataFrame)

from importlib import resources as impresources

import pandas as pd
import pytest

@pytest.fixture
def test_data():
    def _(filename: str) -> pd.DataFrame:
        data_path = impresources.files(__package__) / "soft_sensors/test_data" / filename
        return pd.read_csv(str(data_path))
    return _

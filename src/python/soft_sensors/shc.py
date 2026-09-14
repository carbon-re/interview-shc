import pandas as pd


from src.python.soft_sensors.models import Ok, Fail


def transform(raw_data: pd.DataFrame) -> Ok[pd.DataFrame] | Fail[str]:
    try:
        return Ok(value=raw_data)
    except Exception as e:
        return Fail(value=e.__repr__())


def calculate(transformed_data: pd.DataFrame) -> Ok[pd.DataFrame] | Fail[str]:
    clinker_ratio: float = 1.55

    try:
        transformed_data["shc"] = (
            transformed_data.f_k_coal_tput * transformed_data.f_k_coal_ncv
        ) / (transformed_data.s_ph_sil_tput / clinker_ratio)
        return Ok[transformed_data]
    except Exception as e:
        return Fail[e.__repr__()]

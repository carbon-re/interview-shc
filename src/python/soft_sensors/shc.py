import pandas as pd


def transform(raw_data: pd.DataFrame) -> pd.DataFrame:
    return raw_data


def calculate(transformed_data: pd.DataFrame) -> pd.DataFrame:
    clinker_ratio: float = 1.55

    transformed_data["shc"] = (
        transformed_data.f_k_coal_tput * transformed_data.f_k_coal_ncv
    ) / (transformed_data.s_ph_sil_tput / clinker_ratio)

    return transformed_data

import pandas as pd


class ShcSoftSensor:
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        result = transformed_data.copy()
        result["shc"] = (
            transformed_data["f_k_coal_tput"]
            * transformed_data["f_k_coal_ncv"]
            / (transformed_data["s_ph_sil_tput"] / 1.55)
        )
        return result.drop(labels=["f_k_coal_tput", "f_k_coal_ncv", "s_ph_sil_tput"], axis=1)


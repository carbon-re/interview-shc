import pandas as pd
import math 


class ShcSoftSensor:
    CLINKER_RATIO = 1.55
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        df = transformed_data.copy()
        mass_of_clinker = df["s_ph_sil_tput"] / self.CLINKER_RATIO
        heat = df["f_k_coal_ncv"] * df["f_k_coal_tput"]
        result = heat / mass_of_clinker
        result = result.apply(math.floor)
        df["shc"] = result
        return df

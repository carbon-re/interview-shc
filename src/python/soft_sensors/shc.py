import pandas as pd

CLINKER_RATIO = 1.55

class ShcSoftSensor:
    def transform(self, raw_data: pd.DataFrame) -> dict:
        res = {}

        for i in raw_data:
            row = raw_data.iloc[i]

            ts = row["timestamp"]
            raw_meal = row["s_ph_sil_tput"]
            fuel_mass = row["f_k_coal_tput"]
            ncv = row["f_k_coal_ncv"]

            clinker_mass = raw_meal / CLINKER_RATIO
            heat = fuel_mass * ncv

            shc = heat / clinker_mass

            res[ts] = int(shc)

        return res

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        return transformed_data

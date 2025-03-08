import numpy as np
import pandas as pd

class ShcSoftSensor:

    CLINKER_RATIO = 1.55

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        print(raw_data)
        raw_data["f_k_coal_ncv"] = raw_data["f_k_coal_ncv"].ffill()
        return raw_data[raw_data["s_ph_sil_tput"] > 10]

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        print(transformed_data)
        transformed_data["clinker"] = (transformed_data["s_ph_sil_tput"] * 1000) / 1.55
        transformed_data["energy"] = transformed_data["f_k_coal_tput"] * 1000 * transformed_data["f_k_coal_ncv"]
        transformed_data["shc"] = np.floor(transformed_data["energy"] / transformed_data["clinker"]).astype(int)
        return transformed_data[["timestamp", "shc"]]

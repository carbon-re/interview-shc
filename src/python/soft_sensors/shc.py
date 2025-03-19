import pandas as pd
import numpy as np

class ShcSoftSensor:

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        raw_data["mass_clinker"] = raw_data['s_ph_sil_tput'] / 1.55

        raw_data["heat"] = raw_data['f_k_coal_tput'] * raw_data['f_k_coal_ncv']
        
        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        transformed_data["shc"] = np.floor(transformed_data["heat"] / transformed_data["mass_clinker"]).astype(int)

        return transformed_data

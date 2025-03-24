
import numpy as np
import pandas as pd
class ShcSoftSensor:

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        ncv = raw_data['f_k_coal_ncv']
        fuel = raw_data['f_k_coal_tput']
        raw_meal = raw_data['s_ph_sil_tput']

        raw_data = pd.DataFrame({
            "heat": (ncv * fuel),
            "mass_clinker": (raw_meal/1.55),
            "timestamp": raw_data["timestamp"]
        })

        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        # (ncv * fuel) / (raw_meal/1.55)
        transformed_data['shc'] = np.floor(transformed_data["heat"] / transformed_data["mass_clinker"]).astype(int)
        # transformed_data['shc'] = 749
        return transformed_data

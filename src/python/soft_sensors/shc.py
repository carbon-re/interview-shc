import pandas as pd
import numpy as np
class ShcSoftSensor:

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        raw_data['clinker_mass'] = raw_data['s_ph_sil_tput'] / 1.55 # Assuming clinker ratio is 1.55
        raw_data['heat'] = raw_data["f_k_coal_tput"] * raw_data["f_k_coal_ncv"]
        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        expected = transformed_data['heat'] / transformed_data['clinker_mass']
        transformed_data['shc'] = np.floor(expected).astype(int)
        return transformed_data.drop(columns=['s_ph_sil_tput', 'f_k_coal_tput', 'f_k_coal_ncv'])


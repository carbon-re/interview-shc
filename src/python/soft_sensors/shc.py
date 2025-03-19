import pandas as pd
import numpy as np
class ShcSoftSensor:

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        raw_data["heat"] = raw_data["f_k_coal_tput"]*raw_data["f_k_coal_ncv"]
        raw_data["mass_of_clinker"] = raw_data["s_ph_sil_tput"]/1.55
        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        transformed_data["shc"] = transformed_data["heat"]/transformed_data["mass_of_clinker"]
        transformed_data["shc"] = np.floor(transformed_data["shc"]).astype(int)
        return transformed_data

import pandas as pd
class ShcSoftSensor:

    CLINKER_RATIO = 1.55

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        transformed_data["clinker"] = (transformed_data["s_ph_sil_tput"] * 1000) / 1.55
        transformed_data["energy"] = transformed_data["f_k_coal_tput"] * 1000 * transformed_data["f_k_coal_ncv"]
        transformed_data["shc"] = transformed_data["energy"] / transformed_data["clinker"]
        return transformed_data[["timestamp", "shc"]]

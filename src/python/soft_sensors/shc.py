import numpy as np
import pandas as pd

class ShcSoftSensor:

    CLINKER_RATIO = 1.55

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        raw_data["f_k_coal_ncv"] = raw_data["f_k_coal_ncv"].ffill()

        raw_data["clinker"] = (raw_data["s_ph_sil_tput"] * 1000) / 1.55
        raw_data["energy"] = raw_data["f_k_coal_tput"] * 1000 * raw_data["f_k_coal_ncv"]
        return raw_data[raw_data["s_ph_sil_tput"] > 10]

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        transformed_data["shc"] = np.floor(transformed_data["energy"] / transformed_data["clinker"]).astype(int)
        return transformed_data[["timestamp", "shc"]]

class CdeShcSoftSensor(ShcSoftSensor):

    CLINKER_RATIO = 1.55

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        raw_data["clinker"] = (raw_data["s_ph_sil_tput"] * 1000) / 1.55
        raw_data["energy"] = (raw_data["f_k_coal_tput"] * 1000 * raw_data["f_k_coal_ncv"]) + (raw_data["f_k_rdf_tput"] * 1000 * raw_data["f_k_rdf_ncv"])
        return raw_data[raw_data["s_ph_sil_tput"] > 10]


class DefShcSoftSensor(ShcSoftSensor):

    CLINKER_RATIO = 1.55
    GJ_CONVERSION = 239

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        print(raw_data)
        raw_data["clinker"] = (raw_data["s_ph_sil_tput"] * 1000) / 1.55
        raw_data["energy"] = (raw_data["f_k_petcoke_tput"] * 1000 * raw_data["f_k_petcoke_ncv"]) + (raw_data["f_k_rdf_tput"] * 239000 * raw_data["f_k_rdf_ncv"])
        return raw_data[raw_data["s_ph_sil_tput"] > 10]

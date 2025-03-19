import numpy as np
import pandas as pd


class ShcSoftSensor:
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        transformed_data = raw_data.copy()
        transformed_data["f_k_coal_ncv"] = transformed_data["f_k_coal_ncv"].ffill()
        # transformed_data["energy"] = (
        #     transformed_data["f_k_coal_tput"] * 1000 * transformed_data["f_k_coal_ncv"]
        # )
        transformed_data["energy"] = transformed_data.apply(
            lambda row: row.f_k_coal_tput * 1000 * row.f_k_coal_ncv
            if row.f_k_coal_tput > 0.1
            else None,
            axis=1,
        )
        # transformed_data["clinker_mass"] = (
        #     transformed_data["s_ph_sil_tput"] * 1000 / 1.55
        # )
        print(transformed_data)
        transformed_data["clinker_mass"] = transformed_data.apply(
            lambda row: row.s_ph_sil_tput * 1000 / 1.55
            if row.s_ph_sil_tput > 0.1
            else None,
            axis=1,
        )
        return transformed_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        result = transformed_data.copy()
        result["shc"] = result["energy"] / result["clinker_mass"]
        # result["shc"] = result.apply(lambda row: row["energy"] / result["clinker_mass"] else None
        result["shc"] = np.floor(result["shc"])
        print(result)
        # return pd.DataFrame({"shc": [58, 9]})
        return result


class RdfShcSoftSensor:
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        transformed_data = raw_data.copy()
        # transformed_data["f_k_coal_ncv"] = transformed_data["f_k_coal_ncv"].ffill()
        # transformed_data["energy"] = (
        #     transformed_data["f_k_coal_tput"] * 1000 * transformed_data["f_k_coal_ncv"]
        # )
        transformed_data["coal_energy"] = transformed_data.apply(
            lambda row: row.f_k_coal_tput * 1000 * row.f_k_coal_ncv
            if row.f_k_coal_tput > 0.1
            else 0,
            axis=1,
        )
        transformed_data["rdf_energy"] = transformed_data.apply(
            lambda row: row.f_k_rdf_tput * 1000 * row.f_k_rdf_ncv
            if row.f_k_rdf_tput > 0.1
            else 0,
            axis=1,
        )
        transformed_data["energy"] = (
            transformed_data["coal_energy"] + transformed_data["rdf_energy"]
        )
        # transformed_data["clinker_mass"] = (
        #     transformed_data["s_ph_sil_tput"] * 1000 / 1.55
        # )
        print(transformed_data)
        transformed_data["clinker_mass"] = transformed_data.apply(
            lambda row: row.s_ph_sil_tput * 1000 / 1.55
            if row.s_ph_sil_tput > 0.1
            else None,
            axis=1,
        )
        return transformed_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        result = transformed_data.copy()
        result["shc"] = result["energy"] / result["clinker_mass"]
        # result["shc"] = result.apply(lambda row: row["energy"] / result["clinker_mass"] else None
        result["shc"] = np.floor(result["shc"])
        print(result)
        # return pd.DataFrame({"shc": [58, 9]})
        return result

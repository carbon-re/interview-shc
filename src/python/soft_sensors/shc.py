import pandas as pd

# Mass of raw meal consumed per unit mass of clinker produced.
CLINKER_RATIO = 1.55


class ShcSoftSensor:
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalise plant specific tags onto the canonical column names used by
        `calculate`: `s_ph_sil_tput`, `f_k_coal_tput` and `f_k_coal_ncv`.

        ABC already reports those names in those units, so there is nothing to
        do yet.
        """
        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        """
        Add an `shc` column: specific heat consumption in kcal per kg of
        clinker.

            shc = heat / mass of clinker

        The throughputs are both in t/h, so the kg/t conversion cancels out.
        """
        result = transformed_data.copy()

        heat = result["f_k_coal_tput"] * result["f_k_coal_ncv"]
        clinker = result["s_ph_sil_tput"] / CLINKER_RATIO
e
        result["shc"] = heat / clinker

        return result

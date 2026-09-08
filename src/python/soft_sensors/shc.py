import numpy as np
import pandas as pd

# Tonnes of kiln feed consumed per tonne of clinker produced.
CLINKER_RATIO = 1.55

# Kilograms per tonne, to convert throughputs into mass flows.
KG_PER_TONNE = 1000.0


class ShcSoftSensor:
    """
    Calculates specific heat consumption (kcal/kg of clinker) from kiln feed
    and coal measurements.
    """

    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalise the raw plant CSV into the columns `calculate` expects:
        a timestamp index, plus numeric kiln feed and coal readings.
        """
        transformed = raw_data.copy()
        transformed["timestamp"] = pd.to_datetime(transformed["timestamp"])

        for column in ("s_ph_sil_tput", "f_k_coal_tput", "f_k_coal_ncv"):
            transformed[column] = pd.to_numeric(transformed[column], errors="coerce")

        return transformed.set_index("timestamp").sort_index()

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        """
        Add an `shc` column: the heat released by the coal divided by the mass
        of clinker produced, rounded down to the nearest integer.
        """
        result = transformed_data.copy()

        # kcal/h released by the coal burnt in the kiln.
        total_heat = (
            result["f_k_coal_tput"] * KG_PER_TONNE * result["f_k_coal_ncv"]
        )

        # kg/h of clinker produced from the kiln feed.
        clinker_mass = (result["s_ph_sil_tput"] * KG_PER_TONNE) / CLINKER_RATIO

        shc = total_heat / clinker_mass.replace(0, np.nan)
        result["shc"] = np.floor(shc)

        return result

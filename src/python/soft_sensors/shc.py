import pandas as pd

CLINKER_RATIO = 1.55


class ShcSoftSensor:
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        """Specific heat consumption per timestamp, floored to a whole number."""
        mass_of_clinker = transformed_data.s_ph_sil_tput / CLINKER_RATIO
        heat = transformed_data.f_k_coal_tput * transformed_data.f_k_coal_ncv

        return pd.DataFrame(
            {
                "timestamp": transformed_data.timestamp,
                "shc": (heat // mass_of_clinker).astype(int),
            }
        )

import pandas as pd


class ShcSoftSensor:
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        # timestamp
        # s_ph_sil_tput = raw meal
        # f_k_coal_tput = coal mass
        # f_k_coal_ncv  = coal net calorific value

        return raw_data

    def calculate(self, transformed_data: pd.DataFrame) -> dict[str, int]:
        clinker_ratio = 1.55
        transformed_data['mass_clinker'] = transformed_data['s_ph_sil_tput'] / clinker_ratio
        transformed_data['shc'] = (
            transformed_data['mass_clinker'] * (transformed_data['f_k_coal_tput'] * transformed_data['f_k_coal_ncv'])
        ).astype(int)

        actual_data = transformed_data.set_index('timestamp').to_dict()['shc']
        return actual_data

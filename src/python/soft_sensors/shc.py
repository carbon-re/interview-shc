import numpy as np
import pandas as pd


class ShcSoftSensor:
    def transform(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        raw_meal = raw_data.s_ph_sil_tput
        clinker_ratio = 1.55
        clinker_mass = raw_meal / clinker_ratio

        fuel_mass = raw_data.f_k_coal_tput
        calorific_value = raw_data.f_k_coal_ncv
        heat = fuel_mass * calorific_value

        timestamp = raw_data.timestamp

        transformed_dictionary = {
            "timestamp": timestamp,
            "heat": heat,
            "clinker_mass": clinker_mass,
        }
        transformed_data = pd.DataFrame(transformed_dictionary)

        return transformed_data

    def calculate(self, transformed_data: pd.DataFrame) -> pd.DataFrame:
        heat = transformed_data.heat
        clinker_mass = transformed_data.clinker_mass
        heat_consumption = heat / clinker_mass

        rounded_heat_consumption = heat_consumption.apply(np.floor).astype(int)

        timestamp = transformed_data.timestamp

        heat_consumption_dictionary = {
            "timestamp": timestamp,
            "shc": rounded_heat_consumption,
        }
        heat_consumption_data = pd.DataFrame(heat_consumption_dictionary)

        return heat_consumption_data

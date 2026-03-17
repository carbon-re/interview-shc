import pandas as pd

CLINKER_RATIO = 1.55
TIMESTAMP_COL = "timestamp"
SIL_COL = "s_ph_sil_tput"
COAL_COL = "f_k_coal_tput"
NCV_COL = "f_k_coal_ncv"


class ShcSoftSensor:
    def calculate(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        # iterate over each row to extract values according to known schema
        # check all required data is there
        # send it to the ccalculate function
        result_df = pd.DataFrame(columns=["timestamp", "heat_consumption"])
        for _, row in raw_data.iterrows():
            ts = row[TIMESTAMP_COL]
            sil = row[SIL_COL]
            coal = row[COAL_COL]
            ncv = row[NCV_COL]
            heat_consumption = self.calculate_heat_consumption(
                mass_raw_meal=sil, clinker_ratio=CLINKER_RATIO, mass_fuel=coal, ncv=ncv
            )
            result_df.append([ts, heat_consumption])

        return result_df

    def calculate_heat_consumption(
        self, mass_raw_meal, clinker_ratio, mass_fuel, ncv
    ) -> float:
        return (mass_fuel * ncv) / (mass_raw_meal / clinker_ratio)

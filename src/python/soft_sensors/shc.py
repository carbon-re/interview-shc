import csv
from datetime import datetime

class ShcSoftSensor:
    def __init__(self):
        self._clinker_ratio = 1.55


    def csv_row_reader(self, filepath):
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield {
                    "timestamp": datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    "raw_meal": float(row["s_ph_sil_tput"]),
                    "coal_tph": float(row["f_k_coal_tput"]),
                    "ncv": float(row["f_k_coal_ncv"]),
                }
    
    def convert(self, filepath):
        reader = self.csv_row_reader(filepath, json)

        while next(reader):
            row = next(reader)
            shc = (row["coal_tph"] * 1000 * row["ncv"]) / (row["raw_meal"] / self._clinker_ratio)




    
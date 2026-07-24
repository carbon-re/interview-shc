import pandas as pd
from config.local import config
import math

class shc:

    def __init__(self, input_path):
        self.__path = input_path

    def read_input(self):
        df = pd.read_csv(self.__path)
        # do some validation if file is present and has data
        return df

    def compute(self, df):

        mass_clinker = df['s_ph_sil_tput'] *  config['clinker_ratio']

        heat = df['f_k_coal_tput'] * df['f_k_coal_ncv']

        shc = math.floor(heat / mass_clinker)

        df['shc'] = shc
        result_dict = dict(zip(df['timestamp'] , df['shc']))

        return result_dict




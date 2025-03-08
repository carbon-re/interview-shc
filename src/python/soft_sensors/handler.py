import pandas as pd
from src.python.soft_sensors import shc

import os

def handle(event, context):
    bucket = os.environ["BUCKET"]
    data = pd.read_csv(f's3://{bucket}/abc.csv')
    soft_sensor = shc.ShcSoftSensor()
    return soft_sensor.calculate(data)

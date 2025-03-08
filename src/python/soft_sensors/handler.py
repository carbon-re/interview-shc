import awswrangler as wr
from src.python.soft_sensors import shc

import os

def handle(event, context):
    bucket = os.environ["BUCKET"]
    data = wr.s3.read_csv(f's3://{bucket}/abc.csv')
    soft_sensor = shc.ShcSoftSensor()
    return soft_sensor.calculate(data)

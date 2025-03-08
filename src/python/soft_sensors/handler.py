import awswrangler as wr
from src.python.soft_sensors import shc

import os

def handle(event, context):
    bucket = os.environ["BUCKET"]
    data = wr.s3.read_csv(f's3://{bucket}/abc.csv')
    soft_sensor = shc.ShcSoftSensor()
    result = soft_sensor.calculate(data)
    result = result.set_index("timestamp")
    return result["shc"].to_dict()

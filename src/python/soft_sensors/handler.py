import awswrangler as wr
from src.python.soft_sensors import shc

import os

def handle(event, context):
    bucket = os.environ["BUCKET"]
    plant = event["plant"]
    data = wr.s3.read_csv(f's3://{bucket}/{plant}.csv')
    soft_sensor = shc.CdeShcSoftSensor() if plant == "cde" else shc.ShcSoftSensor()
    data = soft_sensor.transform(data)

    result = soft_sensor.calculate(data)
    result = result.set_index("timestamp")
    return result["shc"].to_dict()

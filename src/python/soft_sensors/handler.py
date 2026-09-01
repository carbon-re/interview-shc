import math

import awswrangler as wr

from src.python.soft_sensors.shc import ShcSoftSensor

# The bucket terraform creates has a random suffix, so it's pinned by hand for now.
# TODO: pass it in as a lambda environment variable instead.
DATA_BUCKET = "cre-data-shc20260901115228361100000001"


def handle(event, context):
    if event["plant"] == "hello":
        return {"message": "Hello, world - updated"}

    raw_data = wr.s3.read_csv(f"s3://{DATA_BUCKET}/{event['plant']}.csv")

    sensor = ShcSoftSensor()
    result = sensor.calculate(sensor.transform(raw_data))

    # Round each value _down_ to the nearest integer. math.floor gives back a plain
    # int, unlike numpy's, so the response is JSON serialisable.
    return {
        timestamp: math.floor(shc)
        for timestamp, shc in zip(result["timestamp"], result["shc"])
    }

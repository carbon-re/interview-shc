import os

import awswrangler as wr
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.python.soft_sensors.shc import ShcSoftSensor

logger = Logger()

BUCKET_ENV_VAR = "DATA_BUCKET"
PREFIX_ENV_VAR = "DATA_PREFIX"


def plant_data_uri(plant: str) -> str:
    """Build the s3 uri of a plant's csv from the configured bucket and prefix."""
    bucket = os.environ[BUCKET_ENV_VAR]
    prefix = os.environ.get(PREFIX_ENV_VAR, "").strip("/")
    key = f"{prefix}/{plant}.csv" if prefix else f"{plant}.csv"
    return f"s3://{bucket}/{key}"


@logger.inject_lambda_context
def handle(event, context: LambdaContext):
    plant = event["plant"]

    uri = plant_data_uri(plant)
    logger.info("Reading plant data", extra={"plant": plant, "uri": uri})

    raw_data = wr.s3.read_csv(uri)
    logger.info("Read plant data", extra={"plant": plant, "rows": len(raw_data)})

    sensor = ShcSoftSensor()
    transformed_data = sensor.transform(raw_data)
    result = sensor.calculate(transformed_data)

    logger.info("Calculated soft sensor", extra={"plant": plant, "rows": len(result)})

    return {timestamp: int(shc) for timestamp, shc in zip(result.timestamp, result.shc)}

import awswrangler as wr

from src.python.soft_sensors.shc import ShcSoftSensor


def handle(event, context):
    if event["plant"] == "abc":
        data = wr.read_csv(path="s3://cre-data-shc20250321113614864500000001/abc.csv")

        sensor = ShcSoftSensor()
        transformed = sensor.transform(data)
        result = sensor.calculate(transformed)

        result.set_index("timestamp")
        result.to_dict("index")

        return result

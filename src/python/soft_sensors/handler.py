import awswrangler as wr
from src.python.soft_sensors.shc import ShcSoftSensor

def handle(event, context):
    bucket_name = "cre-data-shc20250321142629340500000001"
    file_name = event["plant"]
    path = f"s3://{bucket_name}/{file_name}.csv"
    df = wr.s3.read_csv(path)
    sensor = ShcSoftSensor()
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)

    result_dict = {}
    for _, row in result.iterrows():
        result_dict[row["timestamp"]] = row["shc"]

    return result_dict


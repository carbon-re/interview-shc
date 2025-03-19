from src.python.soft_sensors.shc import ShcSoftSensor
import awswrangler
import pandas as pd

BUCKET_PATH = "s3://cre-data-shc20250319110005411800000001/abc.csv"

# AWS Rangler
# URI = s3://cre-data-shc20250319110005411800000001/abc.csv
def handle(event: dict, context):

    data = awswrangler.s3.read_csv(path=BUCKET_PATH)

    data_dict = data_processing(data)

    return data_dict

    # if event["plant"] == "hello":
    #     return {
    #         "message": "Hello, world"
    #     }

def data_processing(data: pd.DataFrame):
    sensor = ShcSoftSensor()

    transformed = sensor.transform(data)
    tranformed_df = sensor.calculate(transformed)

    data_dict = {}
    for _, row in tranformed_df.iterrows():
        data_dict[row["timestamp"]] = row["shc"]

    return data_dict
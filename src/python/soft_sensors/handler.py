from src.python.soft_sensors.shc import ShcSoftSensor

import awswrangler

def handle(event, context):
    bucket_key = "cre-data-shc20250319142721402400000001"
    if event["plant"] == "abc":
        df = awswrangler.s3.read_csv(f"s3://{bucket_key}/abc.csv")
        sensor = ShcSoftSensor()
        transformed = sensor.transform(df)
        result = sensor.calculate(transformed)
        result_shc = result[["timestamp", "shc"]]
        return result_shc.set_index('timestamp')['shc'].to_dict()
        

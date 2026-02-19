from src.python.soft_sensors.shc import ShcSoftSensor

from awswrangler import s3


def handle(event, context):
    if event["plant"] == "hello":
        return {"message": "Hello, world"}
    
    soft_sensor = ShcSoftSensor()

    raw = s3.read_csv(f's3://cre-data-shc20260219111529138400000001/{event["plant"]}.csv')
    transformed = soft_sensor.transform(raw)
    calculated = soft_sensor.calculate(transformed)

    return calculated
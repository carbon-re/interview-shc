from src.python.soft_sensors.shc import ShcSoftSensor
import awswrangler as wr




def handle(event, context):
    p = event["plant"]

    soft_sensors = ShcSoftSensor()

    match p:
        case "abc":
            df = wr.s3.read_csv([f"s3://cre-data-shc20260219134827157400000001/{p}.csv"])
                
            return soft_sensors.transform(df)

from src.python.soft_sensors.shc import ShcSoftSensor
import awswrangler

def handle(event, context):
    bucket_name  = "cre-data-shc20250806093903615100000001"
    
    if event["plant"] == "abc":
        df = awswrangler.s3.read_csv(f's3://{bucket_name}/abc.csv')
        ss = ShcSoftSensor()
        result = ss.calculate(ss.transform(df))
        result = result[["timestamp", "shc"]]
        return result.set_index("timestamp")["shc"].to_dict()
        

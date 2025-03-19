import awswrangler as wr

from src.python.soft_sensors.shc import RdfShcSoftSensor, ShcSoftSensor


def handle(event, context):
    if event["plant"] == "hello":
        return {"message": "Hello, world"}

    plant = event["plant"]
    file = f"s3://cre-data-shc20250319093504423900000001/{event['plant']}.csv"
    # file = f"https://cre-data-shc20250318093403258700000001.s3.eu-west-1.amazonaws.com/{event['plant']}.csv"
    # df = pd.read_csv(file)
    df = wr.s3.read_csv(file)
    if plant in ["cde", "def"]:
        sensor = RdfShcSoftSensor()
    else:
        sensor = ShcSoftSensor()
    result = transform(df, sensor)
    return result


def transform(df, sensor):
    transformed = sensor.transform(df)
    result = sensor.calculate(transformed)
    print(result)
    # result = result[["timestamp", "shc"]]
    # print(result)
    # print(result.to_dict())
    result = result.dropna(subset=["shc"])
    result = dict(zip(result["timestamp"], result["shc"]))
    print(result)
    # return result.to_json()
    # return result.to_dict()
    return result

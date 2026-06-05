from src.python.soft_sensors import SoftSensor
from soft_sensors.jamie import main as shcCalc


def handle(event, context):
    if event["plant"] == "hello":
        return {"message": "Hello, world"}
    else:
        print(shcCalc(event["plant"]))

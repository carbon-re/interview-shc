from src.python.soft_sensors import SoftSensor

def handle(event, context):
    if event["plant"] == "hello":
        return {
            "message": "Hello, world"
        }

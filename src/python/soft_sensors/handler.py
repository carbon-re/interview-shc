from turtle import pd
from src.python.soft_sensors import SoftSensor
import pandas as pd

def handle(event, context):
    if event["plant"] == "hello":
        return {"message": "Hello, world"}



def read_csv(file_path) -> pd.DataFrame:
    return pd.read_csv(file_path)
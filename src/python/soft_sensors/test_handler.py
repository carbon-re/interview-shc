from src.python.soft_sensors.handler import data_processing

def test_data_processing(test_data):
    df = test_data("abc.csv")
    data = data_processing(df)

    result = data["2023-01-01 10:00:00"]

    expected_result = 723

    assert result == expected_result
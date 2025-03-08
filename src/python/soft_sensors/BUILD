python_sources()

python_aws_lambda_function(
    name="lambda",
    handler="src.python.soft_sensors.handler:handle",
    dependencies=[
        "3rdparty/python:reqs#awswrangler",
        "3rdparty/python:reqs#pandas",
    ]
)

python_tests(
    name="tests",
    dependencies=["src/python/soft_sensors/test_data:data"]
)

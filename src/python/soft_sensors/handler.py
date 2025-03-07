def handle(event, context):
    print("hello world")
    return {
        "statusCode": 200,
        "body": "hello world"
    }

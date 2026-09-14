def handle(event, context):
    if event["plant"] == "hello":
        return {"message": "Hello, world"}

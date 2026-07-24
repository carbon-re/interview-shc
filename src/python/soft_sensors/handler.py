from src.python.soft_sensors import SoftSensor


def handle(event, context):
    if event["plant"] == "hello":
        return {"message": "Hello, world"}
    
    #maybe some logic around deciphering the folder/ filename

    #connect to S3 bucket
   
    #separate function for reading file x from folder y
    #take that output pass into below
    #separate function for doing calculations
    
    

    

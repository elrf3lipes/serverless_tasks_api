import json

def handler(event, context):
    # respond to unrecognized routes or methods
    return {
        "statusCode": 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Resource not found"})
    }

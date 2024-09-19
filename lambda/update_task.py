import os
import json
import boto3
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
tracer = Tracer()
app = APIGatewayRestResolver()
dynamodb_client = boto3.client("dynamodb")

@app.put("/tasks/{taskId}")
@tracer.capture_method
def update_task(taskId: str):
    table = os.environ.get("TABLE_NAME")
    
    if not app.current_event.body:
        return app.response(
            status_code=400,
            body={"message": "Missing request body"}
        )

    item = app.current_event.json_body
    
    try:
        dynamodb_client.update_item(
            TableName=table,
            Key={"taskId": {"S": taskId}},
            UpdateExpression="SET title = :title, description = :description, #status = :status",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":title": {"S": item.get("title", "")},
                ":description": {"S": item.get("description", "")},
                ":status": {"S": item.get("status", "")}
            }
        )
        return app.response(
            status_code=200,
            body={"message": "Task updated successfully"}
        )
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return app.response(
            status_code=500,
            body={"message": "Internal server error"}
        )

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)

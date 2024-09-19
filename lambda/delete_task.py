import boto3
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")

def handler(event, context):
    table = os.environ.get("TABLE_NAME")
    task_id = event["pathParameters"].get("taskId")
    
    if not task_id:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Missing taskId in path parameters"})
        }
    
    try:
        dynamodb_client.delete_item(
            TableName=table,
            Key={"taskId": {"S": task_id}}
        )
        return {
            "statusCode": 204,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Task deleted successfully"})
        }
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal server error"})
        }

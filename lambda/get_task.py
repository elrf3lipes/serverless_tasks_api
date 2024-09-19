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
        response = dynamodb_client.get_item(
            TableName=table,
            Key={"taskId": {"S": task_id}}
        )
        item = response.get("Item")
        
        if not item:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Task not found"})
            }
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "taskId": item["taskId"]["S"],
                "title": item["title"]["S"],
                "description": item["description"]["S"],
                "status": item["status"]["S"]
            })
        }
    except Exception as e:
        logger.error(f"Error fetching task: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal server error"})
        }

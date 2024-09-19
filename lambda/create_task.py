import boto3
import os
import json
import logging
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client("dynamodb")

def handler(event, context):
    table = os.environ.get("TABLE_NAME")
    logger.info(f"Loaded table name from environment variable TABLE_NAME: {table}")

    if not event.get("body"):
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Request body is missing"})
        }

    try:
        item = json.loads(event["body"])
        title = item.get("title")
        description = item.get("description")
        status = item.get("status")

        if not all([title, description, status]):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing required fields: title, description, status"})
            }

        task_id = str(uuid.uuid4())
        dynamodb_client.put_item(
            TableName=table,
            Item={
                "taskId": {"S": task_id},
                "title": {"S": title},
                "description": {"S": description},
                "status": {"S": status}
            }
        )

        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "taskId": task_id,
                "title": title,
                "description": description,
                "status": status
            })
        }
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Internal server error"})
        }

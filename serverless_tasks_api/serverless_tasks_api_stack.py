#!/usr/bin/env python3
from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb_,
    aws_lambda as lambda_,
    aws_apigateway as apigw_,
)
from constructs import Construct

class ServerlessTasksApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB Table
        tasks_table = dynamodb_.Table(
            self,
            "TasksTable",
            table_name="TasksTable",
            partition_key=dynamodb_.Attribute(
                name="taskId", type=dynamodb_.AttributeType.STRING
            ),
            read_capacity=5,  # Adjust as needed
            write_capacity=5  # Adjust as needed
        )

        # Lambda Function: Create Task
        create_task_lambda = lambda_.Function(
            self,
            "CreateTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset("lambda"),
            handler="create_task.handler",
            environment={
                "TABLE_NAME": tasks_table.table_name
            }
        )
        tasks_table.grant_write_data(create_task_lambda)

        # Lambda Function: Get Task
        get_task_lambda = lambda_.Function(
            self,
            "GetTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset("lambda"),
            handler="get_task.handler",
            environment={
                "TABLE_NAME": tasks_table.table_name
            }
        )
        tasks_table.grant_read_data(get_task_lambda)

        # Lambda Function: Update Task
        update_task_lambda = lambda_.Function(
            self,
            "UpdateTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset("lambda"),
            handler="update_task.handler",
            environment={
                "TABLE_NAME": tasks_table.table_name
            }
        )
        tasks_table.grant_read_write_data(update_task_lambda)

        # Lambda Function: Delete Task
        delete_task_lambda = lambda_.Function(
            self,
            "DeleteTaskFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset("lambda"),
            handler="delete_task.handler",
            environment={
                "TABLE_NAME": tasks_table.table_name
            }
        )
        tasks_table.grant_read_write_data(delete_task_lambda)

        # Default Lambda Function for unrecognized routes
        default_lambda = lambda_.Function(
            self,
            "DefaultLambdaFunction",
            runtime=lambda_.Runtime.PYTHON_3_10,
            code=lambda_.Code.from_asset("lambda"),
            handler="default.handler"
        )

        # Create API Gateway
        api = apigw_.LambdaRestApi(
            self,
            "TasksApi",
            handler=create_task_lambda,
            proxy=False
        )

        # Create API Gateway Resources and Methods
        tasks = api.root.add_resource("tasks")
        tasks.add_method("POST", apigw_.LambdaIntegration(create_task_lambda))  # Create Task
        tasks.add_method("GET", apigw_.LambdaIntegration(get_task_lambda))    # Get Task

        task = tasks.add_resource("{taskId}")
        task.add_method("PUT", apigw_.LambdaIntegration(update_task_lambda))   # Update Task
        task.add_method("DELETE", apigw_.LambdaIntegration(delete_task_lambda))  # Delete Task

        # Default catch-all integration
        api.root.add_method("ANY", apigw_.LambdaIntegration(default_lambda))


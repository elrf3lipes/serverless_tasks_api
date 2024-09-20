# Welcome to Serverless Tasks API

Serverless CRUD API for tasks using AWS CDK, Lambda, API Gateway, and DynamoDB.

```markdown
## Requisites:
- Node.js
- npm (latest)
- Python (3.x)
- AWS CLI (latest)
- AWS CDK (latest)
- AWS account profile with access key and secret key configured

## Attributes:
- API Gateway that exposes the REST API
- Lambda Functions that handle the CRUD operations
- DynamoDB Table to store task data

## How to deploy
```bash
git clone https://github.com/elrf3lipes/serverless_tasks_api
cd serverless_tasks_api
cdk bootstrap "aws://<account>/<region>"
cdk synth
cdk deploy
```

## How to test using curl:

- **Create a task**:
```bash
curl -X POST https://<api-url>/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description", "status": "pending"}'
```

- **Get a task**:
```bash
curl https://<api-url>/tasks/<taskId>
```

- **Update a task**:
```bash
curl -X PUT https://<api-url>/tasks/<taskId> \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "This task has been updated", "status": "completed"}'
```

- **Delete a task**:
```bash
curl -X DELETE https://<api-url>/tasks/<taskId>
```

- **Example of Curl commands and Responses**:

![Curl Responses](https://github.com/elrf3lipes/ramon-s_portfolio/raw/main/images/curl_responses.png)

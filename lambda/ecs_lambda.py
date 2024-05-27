import json
import csv
import urllib.parse
import boto3
import io

print('Loading function')

s3 = boto3.client('ecs')

import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('ecs')
    response = client.run_task(
        cluster='cloud-project-pipeline',
        launchType='FARGATE',
        taskDefinition='cloud-project-pipeline-v2',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-0169d9e6343f8a1dd',  # Replace with your subnet ID
                    'subnet-07e50de48236c1c32',
                    'subnet-09820407b79b4673f'
                ],
                'assignPublicIp': 'ENABLED'  # 'DISABLED' if you don't need a public IP
            }
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

import json
import csv
import urllib.parse
import boto3
import io
#from io import StringIO

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    destination_bucket = event['Records'][0]['s3']['bucket']['dest_name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    destination_key = key
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])

        s3.put_object(Bucket=destination_bucket, Key=key, Body=response['Body'].read())
        print(f"File {key} copied to {destination_key} ")
        return response['ContentType']
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

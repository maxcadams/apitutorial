import json
import os
 
from . import decimalencoder #relative import
import boto3
 
dynamodb = boto3.resource('dynamodb')
 
def list(event, context):
  table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
 
  result = table.scan()
 
    # create a response
  response = {
        "statusCode": 200,
        #"body": json.dumps(result['Items'])
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
  }
  return response

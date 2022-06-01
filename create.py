import json
import logging
import os
import time
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
 
def create(event, context):
    data = json.loads(event['body'])
    if 'party' not in data:
        logging.error("validation failed")
        raise Exception("Couldn't create the party")
      
    timestamp = str(time.time())
 
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
 
    party = {
      'id': str(uuid.uuid1()),
      'party': data['party'],
      'checked': False,
      'createdAt': timestamp,
      'updatedAt': timestamp,
    }
 
    table.put_item(Item=party)
 
    response = {
      "statusCode": 200,
      "body": json.dumps(party)
    }
    return response

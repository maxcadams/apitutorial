#### wanna test puttin into dynamodb (into table stuff) 

import json
import logging
import os
import time
import uuid
import boto3
from faker import Faker

import decimalencoder

"""
Wraper class that encapsulates functionality of dynamodb code in lambda handlers
"""

FAKER_TEST_SEED = 12345


class DataUtil:

    def create_action(dynamodb, test=False): 
        timestamp = str(time.time())
        
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        fake = Faker()


        # using this because can't figure out how to maintain
        # faker seed within funciton call in test       
        if test: 
            fake.random.seed(FAKER_TEST_SEED)


        party = {
                'id': str(uuid.uuid4()),
                'party': fake.name(),
                'checked': False,
                'createdAt': timestamp,
                'updatedAt': timestamp
            }
        
        return table.put_item(Item=party)


    def get_action(dynamodb, id):
        
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        
        res = table.get_item(
            Key={
                'id': id
            }
        )

        return res['Item']


    def update_action(dynamodb, id, party, checked, updatedAt):

        #timestamp = str(time.time())
 
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
        
        result = table.update_item(
            Key={
                'id': id
            },
            UpdateExpression = "set info.party=:p, info.checked=:c, info.updatedAt=:u",
            ExpressionAttributeValues={
                ':p': party,
                ':c': checked,
                ':u': updatedAt
            },
            ReturnValues="UPDATED_NEW"   
        )

        return result['Attributes']

    def delete_action(dynamodb, id):
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

        res = table.delete_item(
            Key={
                'id': id
            }
        )
        
        return res

    def list_action(dynamodb):
        table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

        result = table.scan()

        return result['Items']

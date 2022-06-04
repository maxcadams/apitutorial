import pytest


import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from ..datautil import DataUtil



def test_create_handler(make_stubber):
    dyn = boto3.resource('dynamodb')
    
    print(make_stubber)
    dyn_stubber = make_stubber(dyn.meta.client) 
    
    resp = DataUtil.create_action(dyn, stub=True, dyn_stubber=dyn_stubber)

    print(resp)

    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200



    


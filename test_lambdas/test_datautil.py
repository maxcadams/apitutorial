import pytest


import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import os

from ..datautil import DataUtil
from faker import Faker
import uuid
import time


TABLE_NAME = 'party-test'
FAKE_NAME = 'John Doe'
FAKE_UUID = 123
FAKE_TIME = 10.0

@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return 12345

def fake_uuid():
    return str(FAKE_UUID)

def fake_uuid1():
    return str(FAKE_UUID * FAKE_UUID)

def fake_time():
    return str(FAKE_TIME)

def fake_update_time():
    return str(FAKE_TIME * FAKE_TIME)


def test_create_handler(make_stubber, monkeypatch, faker):
    dyn = boto3.resource('dynamodb')

    monkeypatch.setenv('DYNAMODB_TABLE', TABLE_NAME)
    #monkeypatch.setattr(Faker.random.getter, 'seed',  faker_seed)
    monkeypatch.setattr(uuid, "uuid4", fake_uuid)
    monkeypatch.setattr(time, "time", fake_time)

    timestamp = str(fake_time())
    name = faker.name()
    id = fake_uuid()
    dyn_stubber = make_stubber(dyn.meta.client) 
   
    party = {
                'id': id,
                'party': name,
                'checked': False,
                'createdAt': timestamp,
                'updatedAt': timestamp
            }
   

    dyn_stubber.stub_put_item(TABLE_NAME, party, http_status=200)

    resp = DataUtil.create_action(dynamodb=dyn, test=True)

    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200


def test_get_handler(make_stubber, monkeypatch, faker):
    dyn = boto3.resource('dynamodb')

    monkeypatch.setenv('DYNAMODB_TABLE', TABLE_NAME)
    #monkeypatch.setattr(Faker.random.getter, 'seed',  faker_seed)
    monkeypatch.setattr(uuid, "uuid4", fake_uuid)
    monkeypatch.setattr(time, "time", fake_time)
   
    timestamp = fake_time()
    name = faker.name()
    id = fake_uuid()
    dyn_stubber = make_stubber(dyn.meta.client)

    in_info = {
        'id': id,
        'party': name,
        'checked': False, 
        'createdAt': timestamp, 
        'updatedAt': timestamp,
    }

    dyn_stubber.stub_get_item(
        TABLE_NAME, {'id': in_info['id']}, in_info)

    out_info = DataUtil.get_action(dyn, in_info['id'])
  
    assert in_info == out_info

def test_update_handler(make_stubber, monkeypatch, faker):
    dyn = boto3.resource('dynamodb')

    monkeypatch.setenv('DYNAMODB_TABLE', TABLE_NAME)
    #monkeypatch.setattr(Faker.random.getter, 'seed',  faker_seed)
    monkeypatch.setattr(uuid, "uuid4", fake_uuid)
    monkeypatch.setattr(time, "time", fake_update_time)
    
    updatetimestamp = fake_update_time()
    faker.seed_instance(5432)
    name = faker.name()
    id = fake_uuid()
    dyn_stubber = make_stubber(dyn.meta.client)
    
    update = {
    'info': {   # formatted w extra nexted entry for stubber
        'party': name,
        'checked': True, 
        'updatedAt': updatetimestamp
        }
    }


    dyn_stubber.stub_update_item(
        TABLE_NAME, {'id': id}, update, 'UPDATED_NEW'
    )

    update_resp = DataUtil.update_action(dyn, id, **update['info'])

    assert update == update_resp



def test_delete_handler(make_stubber, monkeypatch):
    dyn = boto3.resource('dynamodb')

    monkeypatch.setenv('DYNAMODB_TABLE', TABLE_NAME)
    monkeypatch.setattr(uuid, "uuid4", fake_uuid)   

    id = fake_uuid()
    dyn_stubber = make_stubber(dyn.meta.client)

    dyn_stubber.stub_delete_item(
        TABLE_NAME, {'id': id }
    )

    DataUtil.delete_action(dyn, id)
    
    
def test_list_handler(make_stubber, monkeypatch, faker):
    dyn = boto3.resource('dynamodb')

    monkeypatch.setenv('DYNAMODB_TABLE', TABLE_NAME)

    timestamp = fake_time()
    name = faker.name()
    id = fake_uuid()
    dyn_stubber = make_stubber(dyn.meta.client)

    item0 = {
        'id': id,
        'party': name,
        'checked': False, 
        'createdAt': timestamp, 
        'updatedAt': timestamp,
    }  
 
    faker.seed_instance(54321)
    timestamp1 = fake_update_time()
    name1 = faker.name()
    id1 = fake_uuid1()

    item1 = {
        'id': id1,
        'party': name1, 
        'checked': False, 
        'createdAt': timestamp1,
        'updatedAt': timestamp1
    }

    out_items = [item0, item1]

    dyn_stubber.stub_scan(TABLE_NAME, out_items)

    scan_res = DataUtil.list_action(dyn)

    assert scan_res == out_items
    


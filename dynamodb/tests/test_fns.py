import pytest 
from .. import soccerdb 
from decimal import Decimal
import random
from unittest.mock import MagicMock, call

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


dyn = boto3.resource('dynamodb')
db = soccerdb.Footy(dyn)

@pytest.mark.integ
def test_create_table():
    #dyn = boto3.resource('dynamodb')
    
    #initialize DB structure
    table = db.create_table('Clubs')
    
    assert table.name == 'Clubs'
    assert table.table_status == 'CREATING'
    assert db.table != None

@pytest.mark.integ
def test_add_item():
    resp = db.add_item('Real Madrid', 'La Liga', 25, 640.7)
    
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
    assert db.get_item_helper('Real Madrid', 'La Liga')

@pytest.mark.integ
def test_update_item():
    update = {'info': {
        'wins': Decimal(23), 
        'total_revenue': Decimal(str(650.6))
    }}

    update_res = db.update_item('Real Madrid', 'La Liga', 23, 650.6)

    assert update == update_res

@pytest.mark.integ
def test_get_item():
    in_club = {
        'club_name': 'Real Madrid',
        'league': 'La Liga',
        'info': {
            'wins': Decimal(23),
            'total_revenue': Decimal(str(650.6))
        }
    }
    
    out_club = db.get_item(in_club['club_name'], in_club['league'])

    assert in_club == out_club
    assert db.get_item_helper(in_club['club_name'], in_club['league'])

@pytest.mark.integ
def test_delete_item():
    del_key = {
        'club_name': 'Real Madrid',
        'league': 'La Liga'
    }

    db.delete_item(del_key['club_name'], del_key['league'])

    assert not(db.get_item_helper(del_key['club_name'], del_key['league']))


@pytest.mark.integ
def test_delete_table():
    db.delete_table()

    #assert table.table_status == 'DELETING'
    assert db.table == None



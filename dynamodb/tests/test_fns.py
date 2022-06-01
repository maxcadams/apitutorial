import pytest 
from .. import soccerdb 
from decimal import Decimal
import random
from unittest.mock import MagicMock, call

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError




def test_create_table():
    dyn = boto3.resource('dynamodb')
    #initialize DB structure
    db = soccerdb.Footy(dyn)
    table = db.create_table('Clubs')
    
    assert table.name == 'Clubs'
    assert table.table_status == 'CREATING'

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

TABLE_NAME = 'party-test'

class DataUtil:
    
    def create_action(dynamodb, stub=False, dyn_stubber=None): #add table name?
        timestamp = str(time.time())
        

        table = dynamodb.Table(TABLE_NAME)
        fake = Faker()
       
        party = {
                'id': str(uuid.uuid1()),
                'party': fake.name(),
                'checked': False,
                'createdAt': timestamp,
                'updatedAt': timestamp,
            }

        if stub:
            party['id'] = 1

        #print(party)
        
        #stubber acts as  middle ground, so if not input skip this part
        # lets us not log into aws and deploy
        if dyn_stubber is not None:
            print('we here')
            n = dyn_stubber.stub_put_item(TABLE_NAME, party, http_status=200)
                        
                
        return table.put_item(Item=party)

    def get_action(dynamodb, dyn_stubber=None):

        table = dynamodb.Table(TABLE_NAME)





        



    
        
        


        


           
        

        
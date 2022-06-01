
"""
Inspired from Movie tutorial from Amazon. 
"""



from decimal import Decimal
from io import BytesIO
import json
import logging
import os
from pprint import pprint
import requests
from zipfile import ZipFile
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from helper_classes import question

logger = logging.getLogger(__name__)

class Footy:
    """Encapsulates Amazon DynamoDB of football data from England (subject to change)"""
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource
        """
        self.dyn_resource = dyn_resource
        self.table = None

    def table_exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.

        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
                raise
        else:
            self.table = table
        return exists

    def create_table(self, table_name):
        """
        Creates an Amazon DynamoDB table that can be used to store movie data.
        The table uses the release year of the movie as the partition key and the
        title as the sort key.

        :param table_name: The name of the table to create.
        :return: The newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'club_name', 'KeyType': 'HASH'},  # Partition key
                    {'AttributeName': 'league', 'KeyType': 'RANGE'}  # Sort key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'club_name', 'AttributeType': 'S'},
                    {'AttributeName': 'league', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10})
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.table

    def add_item(self, club_name, league, wins, total_revenue):
        """
        Adds club and info to able

        :param club_name: name of club
        :param league: league in which club resides
        :param wins: total number of wins in 2020/2021 season club had
        :param total_revenue: revenue of club in 2020/2021 season (millions, euros)
        """
        try:
            response = self.table.put_item(
                    Item={
                        'club_name': club_name,
                        'league': league,
                        'info': { 'wins': wins, 'total_revenue': Decimal(str(total_revenue))}
                    }
                )
        except ClientError as err:
            logger.error(
                "Couldn't add club %s to table %s. Here's why: %s: %s",
                club_name, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        return response
    
    def update_item(self, club_name, league, wins, total_revenue):
        """
        Updates wins, total revenue within info entry for club in table.

        :param club_name: name of club
        :param league: league in which club resides
        :param wins: total number of wins in 2020/2021 season club had
        :param total_revenue: revenue of club in 2020/2021 season
        :return: Updated fields & values
        """
        try:
            response = self.table.update_item(
                Key={'club_name': club_name, 'league': league},
                UpdateExpression="set info.wins=:w, info.total_revenue=:t",
                ExpressionAttributeValues={
                    ':w': wins, ':t': Decimal(str(total_revenue))
                },
                ReturnValues="UPDATED_NEW")
        except ClientError as err:
            logger.error(
                "Couldn't update club %s to table %s. Here's why: %s: %s",
                club_name, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        return response['Attributes']
    
    def get_item(self, club_name, league):
        """
        Gets club from table given club name and league

        :param club_name: club being queried
        :return: List of clubs with that name (typically one)
        """
        try:
            response = self.table.get_item(Key={'club_name': club_name, 'league': league})
        except ClientError as err:
            logger.error(
                "Couldn't query for club %s. Here's why: %s: %s", year,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        return response['Item']

    def get_item_helper(self, club_name, league):
        """
        Looks for club, club_name, in table. 
        Used for testing purposes

        :param club_name: club being queried
        :return: True if club in table, False if not
        """
        response = self.table.get_item(Key={'club_name': club_name, 'league': league})
        if 'Item' in response.keys():
            return True
        return False



    def delete_item(self, club_name, league):
        """
        Deletes club_name, league entry from table

        :param club_name: name of club
        :param league: league in which club resides
        """
        try:
            self.table.delete_item(Key={'club_name': club_name, 'league': league})
        except ClientError as err:
            logger.error(
                "Couldn't delete club %s. Here's why: %s: %s", club_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def delete_table(self):
        """
        Deletes table
        """
        try: 
            self.table.delete()
            self.table = None
        except ClientError as err:
            logger.error(
                "Couldn't delete table. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise



    
if __name__ == '__main__':
    try:
        dyn_resource = boto3.resource('dynamodb')
        footy = Footy(dyn_resource)
        table = footy.create_table('Clubs')
        footy.add_item('Real Madrid', 'La Liga', 25, 640.7)
        print(footy.get_item_helper('Real Madrid', 'La Liga'))
        footy.delete_table()
    except Exception as e:
        print(f"Something went wrong w demo! Here's what: {e}")

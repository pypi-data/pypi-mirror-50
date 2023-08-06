from __future__ import print_function
import os, boto3
from processor import Processor

DEFAULT_BUFFERS_TABLE_NAME = 'diagnostics-buffer'
DEFAULT_TRIGGERS_TABLE_NAME = 'diagnostics-trigger'

AWS_REGION = os.getenv('TARGET_AWS_REGION', 'eu-west-1')
DYNAMODB_END_URL = 'http://dynamodb.{}.amazonaws.com'.format(AWS_REGION)
BUFFERS_TABLE_NAME = os.getenv('BUFFERS_TABLE_NAME', DEFAULT_BUFFERS_TABLE_NAME)
TRIGGERS_TABLE_NAME = os.getenv('TRIGGERS_TABLE_NAME', DEFAULT_TRIGGERS_TABLE_NAME)

class CloudProcessor(Processor):
    ''' GGProcessor is inherited from base class Processor
        and reimplements few methods related to db handling'''
    def __init__(self, config_file_name, dest_directory, languages=[]):
        self.dest_directory = dest_directory
        self.config_file_name = config_file_name
        self.is_mqtt_buffer = False
        self.is_mqtt_trigger = False
        self.languages = languages
        # Initiate the dynamodb connection
        self.dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION, endpoint_url=DYNAMODB_END_URL)
        self.buffer_table = self.dynamodb.Table(BUFFERS_TABLE_NAME)
        self.trigger_table = self.dynamodb.Table(TRIGGERS_TABLE_NAME)
    
    # Put latest buffer record
    def put_latest_buffer_record(self, serial_number, event_id, hour_counter, level):
        try:
            response = self.buffer_table.put_item(
                Item={
                        'serial_number': serial_number,
                        'level': level,
                        'event_id': event_id,
                        'hour_counter': hour_counter                    
                    }
                )
            print("Response: {}".format(response))
            return True
        except Exception as exc:
            print("Error, Could not put trigger record {}".format(exc))
            
    # Update latest buffer record
    def update_latest_buffer_record(self, serial_number, event_id, hour_counter, level):
        try:
            response = self.buffer_table.update_item(
                Key={
                    'serial_number': serial_number,
                    'level': level
                },
                UpdateExpression="set event_id = :e, hour_counter=:h",
                ExpressionAttributeValues={
                    ':e': event_id,
                    ':h': hour_counter
                },
                ReturnValues="UPDATED_NEW"
            )
            return True
        except Exception as exc:
            print("Error, Could not update buffer record {}".format(exc))


    # Get latest buffer record
    def get_latest_buffer_record(self, serial_number, level):
        try:
            response = self.buffer_table.get_item(
                Key={
                    'serial_number': serial_number,
                    'level': level
                }
            )
            return response['Item']
        except Exception as exc:
            print("Error, Could not get buffer record {}".format(exc))
            return None

    # Put latest trigger record
    def put_latest_trigger_record(self, serial_number, event_id, timestamp, level, duration):
        try:
            response = self.trigger_table.put_item(
                Item={
                        'serial_number': serial_number,
                        'level': level,
                        'event_id': event_id,
                        'timestamp': timestamp,
                        'duration': duration
                    }
                )
            return True
        except Exception as exc:
            print("Error, could not put trigger record {}".format(exc))
            return False
            
    # Put latest trigger record
    def update_latest_trigger_record(self, serial_number, event_id, timestamp, level, duration):
        try:
            response = self.trigger_table.update_item(
                Key={
                    'serial_number': serial_number,
                    'level': level
                },
                UpdateExpression="set event_id=:e, #ts=:t, #dn=:d",
                ExpressionAttributeValues={
                    ':e': event_id,
                    ':t': timestamp,
                    ':d': duration
                },
                ExpressionAttributeNames={
                    "#ts": "timestamp",
                    "#dn": "duration"
                },
                ReturnValues="UPDATED_NEW"
            )
            return True
        except Exception as exc:
            print("Error, Couldn not update trigger record: {}".format(exc))
            return False

    # Get latest trigger record
    def get_latest_trigger_record(self, serial_number, level):
        try:
            response = self.trigger_table.get_item(
                Key={
                    'serial_number': serial_number,
                    'level': level
                }
            )
            return response['Item']
        except Exception as exc:
            print('Error, Could not get trigger record {}'.format(exc))
            return None

            
       
    
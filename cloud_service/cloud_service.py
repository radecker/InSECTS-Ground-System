#!/usr/bin/env python3

from TCPClient import TCPClient
from UDPClient import UDPClient
from BaseApp import BaseApp
import message_pb2 as proto
import boto3
import threading
import datetime
import time


class CloudService(BaseApp):
    def __init__(self, table_name) -> None:
        self.table_name = table_name
        self.db = None
        self.table = None
        self.client = None
        super().__init__("ground.cloud_service")

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'Sensor_Id':"1"
            }
        )
        return response

    def put(self, Sensor_Id='' , Temperature='' , Date='' , Time=''):
        self.table.put_item(
            Item={
                'Sensor_Id':Sensor_Id,
                'Temperature':Temperature,
                'Date' :Date,
                'Time' :Time
            }
        )

    def delete(self,Sensor_Id=''):
        self.table.delete_item(
            Key={
                'Sensor_Id': Sensor_Id
            }
        )

    def describe_table(self):
        response = self.client.describe_table(
            TableName='Sensor'
        )
        return response

    def push_to_cloud(self, msg: proto.Message):
        id = msg.telemetry.temperature_data.sensor_id
        temp = msg.telemetry.temperature_data.sensor_value
        now = datetime.datetime.now()
        date=now.strftime('%Y-%m-%d')
        ctime=now.strftime('%H:%M:%S %Z')
        if self.config_params.connect_to_database:
            self.put(Sensor_Id=str(id), Temperature=str(temp), Date=str(date), Time=str(ctime))
        print(f"Uploaded Sample on Cloud Id:{id} T:{temp} D:{date} T:{ctime}")

    def setup(self):
        if self.config_params.connect_to_database:
            self.db = boto3.resource('dynamodb')
            self.table = self.db.Table(self.table_name)
            self.client = boto3.client('dynamodb')
        else:
            pass

    def run(self):
        # Grab the latest telemetry and push to database
        if len(self.telemetry_queue):
            for msg in self.telemetry_queue:
                if msg.HasField("telemetry"):
                    self.push_to_cloud(msg)

    def shutdown(self):
        pass


if __name__ == "__main__":
    CloudService("DHT")   # Runs the service
    
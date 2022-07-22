#!/usr/bin/env python3

from TCPClient import TCPClient
from UDPClient import UDPClient
from BaseApp import BaseApp
import message_pb2 as proto
import boto3
import threading
import time


class CloudService(BaseApp):
    def __init__(self, table_name) -> None:
        self.table_name = table_name
        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(table_name)
        self.client = boto3.client('dynamodb')
        super().__init__("ground.cloud_service")

    @property
    def get(self):
        response = self.table.get_item(
            Key={
                'Sensor_Id':"1"
            }
        )
        return response

    def put(self, Sensor_Id='' , Temperature='' , Humidity='' , Date='' , Time=''):
        self.table.put_item(
            Item={
                'Sensor_Id':Sensor_Id,
                'Temperature':Temperature,
                'Humidity' :Humidity,
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

    @staticmethod
    def sensor_value():
        pin = 23
        sensor = Adafruit_DHT.DHT11
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        now = datetime.datetime.now()
        date=now.strftime('%Y-%m-%d')
        time=now.strftime('%H:%M:%S %Z')
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity) + 'Date=' + date + ' Time=' + time)
        else:
            print('Failed to get reading. Try again!')
        return temperature, humidity, date, time

    def setup(self):
        pass

    def run(self):
        global counter

        threading.Timer(interval=10, function=self.run).start()
        Temperature , Humidity , Date, Time = obj.sensor_value()
        obj.put(Sensor_Id=str(counter), Temperature=str(Temperature), Humidity=str(Humidity), Date=str(Date), Time=str(Time))
        counter = counter + 1
        print("Uploaded Sample on Cloud T:{},H{} ".format(Temperature, Humidity) + 'D:' + Date + ' T:' + Time )

    def shutdown(self):
        pass


if __name__ == "__main__":
    CloudService()   # Runs the service
    
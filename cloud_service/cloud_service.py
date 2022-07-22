#!/usr/bin/env python3

from TCPClient import TCPClient
from UDPClient import UDPClient
from BaseApp import BaseApp
import message_pb2 as proto
import time


class CloudService(BaseApp):
    def __init__(self) -> None:
        super().__init__("ground.cloud_service")

    def setup(self):
        print(self.config_params)

    def run(self):
        pass

    def shutdown(self):
        pass


if __name__ == "__main__":
    CloudService()   # Runs the service
    
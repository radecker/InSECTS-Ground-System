#!/usr/bin/env python3

from TCPClient import TCPClient
from UDPClient import UDPClient
from BaseApp import BaseApp
import message_pb2 as proto
import time


class AutonomyApp(BaseApp):
    def __init__(self) -> None:
        super().__init__("vehicle.autonomy_app")

    def setup(self):
        print("SETUP!")
        print(self.config_params)

    def run(self):
        print("Autonomy Run!")
        # Check for command messages
        # Check for telemetry messages
        time.sleep(1)


if __name__ == "__main__":
    AutonomyApp()   # Runs the app
    
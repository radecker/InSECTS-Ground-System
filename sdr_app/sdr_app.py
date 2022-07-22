#!/usr/bin/env python3

from BaseApp import BaseApp
from TCPClient import TCPClient
import message_pb2 as proto
import time
import queue

"""
Purpose: This app is used to connect the ground system to the vehicle via SDR or simulation
"""

class SDRApp(BaseApp):
    def __init__(self, id: str) -> None:
        self.tcp_client = None
        self.tcp_send_queue = queue.Queue()
        super().__init__(id)

    def setup(self):
        ip = self.config_params.sdr_tcp_client_ip
        port = self.config_params.sdr_tcp_client_port
        self.tcp_client = TCPClient(ip=ip, port=port, sender="vehicle.sdr_app")
        self.tcp_client.start()

    def run(self):
        if len(self.command_queue):
            for msg in self.command_queue:
                if "ground." in msg.destination or "all" == msg.destination:
                    self.tcp_client.send(msg=msg, dst=msg.destination)
        if len(self.telemetry_queue):
            for msg in self.telemetry_queue:
                if "ground." in msg.destination or "all" == msg.destination:
                    self.tcp_client.send(msg=msg, dst=msg.destination)

    def shutdown(self):
        pass


if __name__ == "__main__":
    SDRApp()
#!/usr/bin/env python3

from tcp_server import TCPServer
from udp_client import UDPClient
import message_pb2 as proto
import time



if __name__ == "__main__":
    udp_client = UDPClient()
    udp_client.add_listener("224.1.1.1", 5050)
    while True:
        messages = udp_client.get_messages()
        for msg in messages:
            print(f"Message: {msg}")
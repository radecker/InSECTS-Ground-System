#!/usr/bin/env python3

from tcp_server import TCPServer
from udp_client import UDPClient
import message_pb2 as proto
import time


if __name__ == "__main__":
    done = False
    server = TCPServer(ip="127.0.0.1", port=5052, sender="ground.sdr_app")
    server.start()
    msg = proto.Message()
    while True:
        messages = server.get_messages()
        for msg in messages:
            print(f"Received: {msg}")
            if not done:
                time.sleep(2)
                server.send(msg=msg, dst="autonomy")
                done = True
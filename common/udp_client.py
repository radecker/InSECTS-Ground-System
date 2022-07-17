#!/usr/bin/env python3

import queue
import message_pb2 as proto
import socket 
import threading
import time
import queue
import struct


class UDPClient():
    def __init__(self, id: str) -> None:
        self.addresses = dict()
        self.id = id

        self.listen_all = False

        self.__sock = None
        self.__address = None
        self.__receive_queue = queue.Queue()
        self.__send_queues = dict()
        self.__header_len = 64
        self.__header_format = 'utf-8'

    def add_listener(self, group: str, port: int) -> None:
        self.addresses[group] = port
        thread = threading.Thread(target=self.__connect, args=(group, port))
        thread.start()

    def __connect(self, group: str, port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.listen_all:
            sock.bind(('', port))
        else:
            sock.bind((group, port))
        mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.__receive(sock)

    def __receive(self, sock) -> None:
        while True:
            msg_len = sock.recv(self.__header_len).decode(self.__header_format)
            if msg_len:
                data = sock.recv(int(msg_len))
                msg = proto.Message()
                msg.ParseFromString(data)
                self.__receive_queue.put(msg)
        sock.close()

    def send(self, msg: proto.Message, group: str, port: int, destination="all") -> None:
        msg.sender = self.id
        msg.destination = destination
        if not (group, port) in self.__send_queues:
            print(f"[UDP Client] ERROR: first add listener on {group, port}")
        else:
            self.__send_queues[(group, port)].put(msg)

    def add_sender(self, group: str, port: int) -> None:
        self.__send_queues[(group, port)] = queue.Queue()
        thread = threading.Thread(target=self.__add_sender, args=(group, port))
        thread.start()

    def __add_sender(self, group: str, port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2) # Might need to change 2
        while True:
            if not self.__send_queues[(group, port)].empty():
                data = self.__send_queues[(group, port)].get().SerializeToString()
                msg_len = len(data)
                send_length = str(msg_len).encode(self.__header_format)
                send_length += b' ' * (self.__header_len - len(send_length))
                sock.sendto(send_length, (group, port))
                sock.sendto(data, (group, port))

    def get_messages(self) -> proto.Message:
        buf = []
        # Reads all messages in queue in FIFO manner
        while not self.__receive_queue.empty():
            buf.append(self.__receive_queue.get())
        return buf


if __name__ == "__main__":
    print("[UDP Client] starting up...")
    client = UDPClient()
    client.add_listener(group="224.1.1.1", port=5050)
    time.sleep(2)
    client.add_sender(group="224.1.1.1", port=5050)
    msg = proto.Message()
    client.send(msg, group="224.1.1.1", port=5050)
    while True:
        messages = client.get_messages()
        for msg in messages:
            print(f"Message: {msg}")
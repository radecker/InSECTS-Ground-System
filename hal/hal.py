#!/usr/bin/env python3

# External Dependencies
import RPi.GPIO as GPIO
import serial

import time
import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

arduino = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=1)

def write_read(val):
    arduino.write(bytes(val, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readlines()
    return data

def blink_led():
    # GPIO Pin setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)

    # Blink LED on and off 10 times
    for i in range(0,10):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
            # blink_led()
            value = write_read("1")
            print(value)





# if len(sys.argv) != 3:
#     print(f"Usage: {sys.argv[0]} <host> <port>")
#     sys.exit(1)

# host, port = sys.argv[1], int(sys.argv[2])
host, port = "127.0.0.1", 44321
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
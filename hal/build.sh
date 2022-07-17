#!/bin/bash
set -e
set -o pipefail

# Copy in the latest protobuf messages 
cp ../common/message_pb2.py .
cp ../common/tcp_client.py .
cp ../common/tcp_server.py .
cp ../common/udp_client.py .

# Build the docker image and tag it
docker build -t hal .
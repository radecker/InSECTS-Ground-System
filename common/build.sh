#!/bin/bash
set -e
set -o pipefail

# Compile protobuf messages and generate new classes
protoc -I=. --python_out=. message.proto
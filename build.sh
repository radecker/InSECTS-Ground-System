#!/bin/bash
set -e
set -o pipefail

# Run the common library build first
cd common/
./build.sh

# Build each individual app
cd ../sdr_app/
./build.sh
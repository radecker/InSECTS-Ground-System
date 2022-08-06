#!/bin/bash
docker run -v /home/jhu-ep/InSECTS-Ground-System/main_service/config.yaml:/usr/src/app/config.yaml:ro --network=host ground.main_service
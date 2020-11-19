#!/usr/bin/env bash

python -m grpc_tools.protoc --proto_path=./protos --python_out=./generated --grpc_python_out=./generated ./protos/echo.proto

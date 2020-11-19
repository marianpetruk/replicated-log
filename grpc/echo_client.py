from __future__ import print_function
import logging

import grpc

import echo_pb2
import echo_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = echo_pb2_grpc.EchoStub(channel)
        # response = stub.SayHello(echo_pb2.HelloRequest(name='you'))
        # print("Greeter client received: " + response.message)

        value = "payload (test message)"
        request = echo_pb2.EchoRequest(message=value)
        response = stub.Reply(request)
        print(f"Response from the server: '{response.message}'")

        # assert response.message == f'You said: {value}'


if __name__ == '__main__':
    logging.basicConfig(level=10)
    run()

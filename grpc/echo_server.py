from concurrent import futures
import logging

import grpc

import echo_pb2_grpc

from grpc.grpc_utils import Echoer


# def SayHello(self, request, context):
#     return echo_pb2.HelloReply(message=f'Hello, {request.name}! (reply from server)')


class EchoServer(echo_pb2_grpc.EchoServicer):
    @staticmethod
    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        echo_pb2_grpc.add_EchoServicer_to_server(Echoer(), server)
        server.add_insecure_port('[::]:50051')
        print("Start server")
        server.start()
        server.wait_for_termination()


if __name__ == '__main__':
    print("Begin loading server")
    logging.basicConfig(level=10)
    EchoServer.serve()

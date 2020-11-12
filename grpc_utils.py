from generated import echo_pb2_grpc, echo_pb2


class Echoer(echo_pb2_grpc.EchoServicer):

    def Reply(self, request, context):
        print(f"on Server meessage received: '{request.message}'. Will echo it back to client.")
        return echo_pb2.EchoReply(message=f"You said: '{request.message}'")

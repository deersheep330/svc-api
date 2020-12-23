from service.api import database_pb2_grpc
import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
if __name__ == '__main__':
    channel = grpc.insecure_channel('localhost:50051')
    stub = database_pb2_grpc.DatabaseStub(channel)
    arr = stub.get_symbols(google_dot_protobuf_dot_empty__pb2.Empty())
    for i in arr:
        print(i)

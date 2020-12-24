from api.protos import database_pb2_grpc
import grpc
from google.protobuf.empty_pb2 import Empty

if __name__ == '__main__':

    channel = grpc.insecure_channel('localhost:50051')
    stub = database_pb2_grpc.DatabaseStub(channel)

    try:
        arr = stub.get_symbols(Empty())
        for i in arr:
            print(i.symbol, i.name)
    except grpc.RpcError as e:
        print(e.details())
        status_code = e.code()
        status_code.name
        status_code.value

        print(status_code.name, status_code.value)

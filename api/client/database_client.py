from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Symbol, SymbolPair
import grpc
from google.protobuf.empty_pb2 import Empty

channel = grpc.insecure_channel('localhost:50051')
stub = database_pb2_grpc.DatabaseStub(channel)

def get_symbols():
    try:
        symbols = stub.get_symbols(Empty())
        for symbol in symbols:
            print(symbol.symbol, symbol.name)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

def get_symbol(symbol):
    try:
        symbol = stub.get_symbol(Symbol(symbol=symbol))
        print(symbol.symbol, symbol.name)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

def upsert_symbols(symbol_pairs):
    try:
        arr = [
            SymbolPair(symbol='AAPL', name='蘋果'),
            SymbolPair(symbol='2303', name='聯電'),
            SymbolPair(symbol='2330', name='台積電')
        ]
        rowcount = stub.upsert_symbols((y for y in arr))
        print(rowcount)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

if __name__ == '__main__':

    #get_symbol('AAPL')
    upsert_symbols({})

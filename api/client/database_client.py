from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Symbol, Stock
import grpc
from google.protobuf.empty_pb2 import Empty

channel = grpc.insecure_channel('localhost:50051')
stub = database_pb2_grpc.DatabaseStub(channel)

def get_stocks():
    try:
        symbols = stub.get_stocks(Empty())
        for symbol in symbols:
            print(symbol.symbol, symbol.name)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

def get_stock(symbol):
    try:
        symbol = stub.get_stock(Symbol(symbol=symbol))
        print(symbol.symbol, symbol.name)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

def upsert_stocks(_dict):
    try:
        rowcount = stub.upsert_stocks((Stock(symbol=key, name=value) for key,value in _dict.items()))
        print(rowcount)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

if __name__ == '__main__':

    get_stocks()
    #get_stock('AAPL')
    '''
    _dict = {
        'AAPL': '蘋果1',
        '2330': '台積電1',
        '2303': '聯電1'
    }
    upsert_stocks(_dict)
    '''
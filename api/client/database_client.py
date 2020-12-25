from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Symbol, Stock, TrendWithDefaultDate, BoughtOrSold
import grpc
from google.protobuf.empty_pb2 import Empty
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
from datetime import timedelta

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

def insert_ptt_trend(_dict):
    try:
        rowcount = stub.insert_ptt_trend(TrendWithDefaultDate(symbol=_dict['symbol'], popularity=_dict['popularity']))
        print(rowcount)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

def insert_reunion_trend(_dict):
    try:
        rowcount = stub.insert_reunion_trend(TrendWithDefaultDate(symbol=_dict['symbol'], popularity=_dict['popularity']))
        print(rowcount)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

def insert_twse_over_bought(_dict):
    try:
        rowcount = stub.insert_twse_over_bought(BoughtOrSold(
            symbol=_dict['symbol'],
            date=_dict['date'],
            quantity=_dict['quantity']
        ))
        print(rowcount)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

def insert_twse_over_sold(_dict):
    try:
        rowcount = stub.insert_twse_over_sold(BoughtOrSold(
            symbol=_dict['symbol'],
            date=_dict['date'],
            quantity=_dict['quantity']
        ))
        print(rowcount)
    except grpc.RpcError as e:
        status_code = e.code()
        print(e.details())
        print(status_code.name, status_code.value)

if __name__ == '__main__':

    #get_stocks()
    #get_stock('AAPL')
    '''
    _dict = {
        'AAPL': '蘋果',
        '2330': '台積電',
        '2303': '聯電'
    }
    upsert_stocks(_dict)
    '''
    '''
    insert_ptt_trend({
        'symbol': 'AAPL',
        'popularity': 666
    })
    '''
    '''
    insert_reunion_trend({
        'symbol': 'RHP',
        'popularity': 350
    })
    '''
    '''
    timestamp = Timestamp()
    today = datetime.datetime.now() - timedelta(days=180)
    timestamp.FromDatetime(today)
    insert_twse_over_bought({
        'symbol': 'T',
        'date': timestamp,
        'quantity': 3600
    })
    '''
    timestamp = Timestamp()
    today = datetime.datetime.now() - timedelta(days=90)
    timestamp.FromDatetime(today)
    insert_twse_over_sold({
        'symbol': 'O',
        'date': timestamp,
        'quantity': 1200
    })

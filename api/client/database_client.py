import grpc
import datetime
from datetime import timedelta
import unittest

from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Symbol, Stock, TrendWithDefaultDate, BoughtOrSold
from api.protos.protobuf_datatype_utils import Empty, Timestamp

from api.utils import get_grpc_hostname

class TestGRPCClient(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        channel = grpc.insecure_channel(f'{get_grpc_hostname()}:6565')
        self.stub = database_pb2_grpc.DatabaseStub(channel)

    def test_get_stocks(self):
        try:
            symbols = self.stub.get_stocks(Empty())
            print(f'get {len(list(symbols))} symbols')
            #for symbol in symbols:
            #    print(symbol.symbol, symbol.name)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_get_stock(self):
        symbol = 'AAPL'
        try:
            symbol = self.stub.get_stock(Symbol(symbol=symbol))
            print(symbol.symbol, symbol.name)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_upsert_stocks(self):
        _dict = {
            'AAPL': '蘋果',
            '2330': '台積電',
            '2303': '聯電'
        }
        try:
            rowcount = self.stub.upsert_stocks((Stock(symbol=key, name=value) for key,value in _dict.items()))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_ptt_trend(self):
        _dict = {
            'symbol': 'AAPL',
            'popularity': 666
        }
        try:
            rowcount = self.stub.insert_ptt_trend(TrendWithDefaultDate(symbol=_dict['symbol'], popularity=_dict['popularity']))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_reunion_trend(self):
        _dict = {
            'symbol': 'RHP',
            'popularity': 350
        }
        try:
            rowcount = self.stub.insert_reunion_trend(TrendWithDefaultDate(symbol=_dict['symbol'], popularity=_dict['popularity']))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_twse_over_bought(self):
        timestamp = Timestamp()
        today = datetime.datetime.now() - timedelta(days=180)
        timestamp.FromDatetime(today)
        _dict = {
            'symbol': 'T',
            'date': timestamp,
            'quantity': 3600
        }
        try:
            rowcount = self.stub.insert_twse_over_bought(BoughtOrSold(
                symbol=_dict['symbol'],
                date=_dict['date'],
                quantity=_dict['quantity']
            ))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_twse_over_sold(self):
        timestamp = Timestamp()
        today = datetime.datetime.now() - timedelta(days=90)
        timestamp.FromDatetime(today)
        _dict = {
            'symbol': 'O',
            'date': timestamp,
            'quantity': 1200
        }
        try:
            rowcount = self.stub.insert_twse_over_sold(BoughtOrSold(
                symbol=_dict['symbol'],
                date=_dict['date'],
                quantity=_dict['quantity']
            ))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_fugle_over_bought(self):
        timestamp = Timestamp()
        today = datetime.datetime.now() - timedelta(days=45)
        timestamp.FromDatetime(today)
        _dict = {
            'symbol': 'TOT',
            'date': timestamp,
            'quantity': 400
        }
        try:
            rowcount = self.stub.insert_fugle_over_bought(BoughtOrSold(
                symbol=_dict['symbol'],
                date=_dict['date'],
                quantity=_dict['quantity']
            ))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_fugle_over_sold(self):
        timestamp = Timestamp()
        today = datetime.datetime.now() - timedelta(days=45)
        timestamp.FromDatetime(today)
        _dict = {
            'symbol': 'CCL',
            'date': timestamp,
            'quantity': 4000
        }
        try:
            rowcount = self.stub.insert_fugle_over_sold(BoughtOrSold(
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

    unittest.main()

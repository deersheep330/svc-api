import grpc
import datetime
from datetime import timedelta
import unittest

from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Symbol, Stock, TrendWithDefaultDate, BoughtOrSold, StockPrice
from api.protos.protobuf_datatype_utils import Empty, Timestamp, datetime_to_timestamp

from api.utils import get_grpc_hostname

class TestGRPCClient(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        channel = grpc.insecure_channel(f'{get_grpc_hostname()}:6565')
        self.stub = database_pb2_grpc.DatabaseStub(channel)

    def test_get_stocks(self):
        try:
            symbols = self.stub.get_stocks(Empty())
            # read the stream result would cause read ptr shifting!
            # and then cause the result cannot be read again!
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
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=180))
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
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=90))
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

    def test_query_twse_over_bought_by_date(self):
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=1))
        try:
            res = self.stub.query_twse_over_bought_by_date(timestamp)
            for item in res:
                print(item.symbol, item.date.ToDatetime().date(), item.quantity)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_query_twse_over_sold_by_date(self):
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=1))
        try:
            res = self.stub.query_twse_over_sold_by_date(timestamp)
            for item in res:
                print(item.symbol, item.date.ToDatetime().date(), item.quantity)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_fugle_over_bought(self):
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=45))
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
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=22))
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

    def test_insert_twse_open_price(self):
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=60))
        _dict = {
            'symbol': '2330',
            'date': timestamp,
            'price': 500.5
        }
        try:
            rowcount = self.stub.insert_twse_open_price(StockPrice(
                symbol=_dict['symbol'],
                date=_dict['date'],
                price=_dict['price']
            ))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_twse_close_price(self):
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=30))
        _dict = {
            'symbol': '2303',
            'date': timestamp,
            'price': 12
        }
        try:
            rowcount = self.stub.insert_twse_close_price(StockPrice(
                symbol=_dict['symbol'],
                date=_dict['date'],
                price=_dict['price']
            ))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)

    def test_insert_us_close_price(self):
        timestamp = datetime_to_timestamp(datetime.datetime.now() - timedelta(days=20))
        _dict = {
            'symbol': 'AAPL',
            'date': timestamp,
            'price': 12.33
        }
        try:
            rowcount = self.stub.insert_us_close_price(StockPrice(
                symbol=_dict['symbol'],
                date=_dict['date'],
                price=_dict['price']
            ))
            print(rowcount)
        except grpc.RpcError as e:
            status_code = e.code()
            print(e.details())
            print(status_code.name, status_code.value)


if __name__ == '__main__':

    unittest.main()

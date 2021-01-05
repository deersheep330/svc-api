from concurrent import futures

from api.utils import get_db_hostname
from api.db import create_engine, start_session, upsert, insert
from api.models import Stock as StockModel
from api.models import PttTrend, ReunionTrend, TwseOverBought, TwseOverSold, FugleOverBought, FugleOverSold
from api.models import TwseOpenPrice, TwseClosePrice, UsClosePrice
from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Stock, RowCount

import grpc

class DatabaseServer(database_pb2_grpc.DatabaseServicer):

    def __init__(self):
        self.engine = create_engine('mysql+pymysql', 'root', 'admin', get_db_hostname(), '3306', 'mydb')

    def get_stocks(self, request, context):
        session = start_session(self.engine)
        try:
            arr = session.query(StockModel).all()
            for item in arr:
                print(item.symbol, item.name)
                yield Stock(symbol=item.symbol, name=item.name)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def get_stock(self, request, context):
        session = start_session(self.engine)
        try:
            symbol = session.query(StockModel).filter_by(symbol=request.symbol).first()
            return Stock(symbol=symbol.symbol, name=symbol.name)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def upsert_stocks(self, request_iterator, context):
        session = start_session(self.engine)
        try:
            rows = []
            for stock in request_iterator:
                rows.append([stock.symbol, stock.name])
                #print(stock.symbol, stock.name)
            rowcount = upsert(session, StockModel, rows)
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_ptt_trend(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, PttTrend, {
                'symbol': request.symbol,
                'popularity': request.popularity
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_reunion_trend(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, ReunionTrend, {
                'symbol': request.symbol,
                'popularity': request.popularity
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_twse_over_bought(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, TwseOverBought, {
                'symbol': request.symbol,
                'date': request.date.ToDatetime(),
                'quantity': request.quantity
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_twse_over_sold(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, TwseOverSold, {
                'symbol': request.symbol,
                'date': request.date.ToDatetime(),
                'quantity': request.quantity
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_fugle_over_bought(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, FugleOverBought, {
                'symbol': request.symbol,
                'date': request.date.ToDatetime(),
                'quantity': request.quantity
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_fugle_over_sold(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, FugleOverSold, {
                'symbol': request.symbol,
                'date': request.date.ToDatetime(),
                'quantity': request.quantity
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_twse_open_price(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, TwseOpenPrice, {
                'symbol': request.symbol,
                'date': request.date.ToDatetime(),
                'price': request.price
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_twse_close_price(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, TwseClosePrice, {
                'symbol': request.symbol,
                'date': request.date.ToDatetime(),
                'price': request.price
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def insert_us_close_price(self, request, context):
        session = start_session(self.engine)
        try:
            rowcount = insert(session, UsClosePrice, {
                'symbol': request.symbol,
                'date': request.date.ToDatetime(),
                'price': request.price
            })
            session.commit()
            return RowCount(rowcount=rowcount)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServicer_to_server(DatabaseServer(), server)
    server.add_insecure_port('[::]:6565')
    server.start()
    server.wait_for_termination()

from concurrent import futures

from api.db import get_db_hostname, create_engine, start_session, upsert, insert
from api.models import Stock as StockModel
from api.models import PttTrend, ReunionTrend, TwseOverBought, TwseOverSold, FugleOverBought, FugleOverSold
from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Stock, RowCount

import grpc

engine = create_engine('mysql+pymysql', 'root', 'admin', get_db_hostname(), '3306', 'mydb')

class DatabaseServer(database_pb2_grpc.DatabaseServicer):

    def __init__(self):
        pass

    def get_stocks(self, request, context):
        session = start_session(engine)
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
        session = start_session(engine)
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
        session = start_session(engine)
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
        session = start_session(engine)
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
        session = start_session(engine)
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
        session = start_session(engine)
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
        session = start_session(engine)
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
        session = start_session(engine)
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
        session = start_session(engine)
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServicer_to_server(
        DatabaseServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

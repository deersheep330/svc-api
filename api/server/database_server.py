from concurrent import futures

from api.db import get_db_hostname, create_engine, start_session, upsert, insert
from api.models import Stock as StockModel
from api.models import PttTrend
from api.protos import database_pb2_grpc
from api.protos.database_pb2 import Stock, RowCount

import grpc

engine = create_engine('mysql+pymysql', 'root', 'admin', get_db_hostname(), '3306', 'mydb')

class DatabaseServer(database_pb2_grpc.DatabaseServicer):

    def __init__(self):
        pass

    def get_stocks(self, request, context):
        try:
            session = start_session(engine)
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
        try:
            session = start_session(engine)
            symbol = session.query(StockModel).filter_by(symbol=request.symbol).first()
            return Stock(symbol=symbol.symbol, name=symbol.name)
        except Exception as e:
            print(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
        finally:
            session.close()

    def upsert_stocks(self, request_iterator, context):
        try:
            session = start_session(engine)
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
        try:
            session = start_session(engine)
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


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServicer_to_server(
        DatabaseServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

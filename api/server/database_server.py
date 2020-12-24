from concurrent import futures

from api.db import get_db_hostname, create_engine, start_session
from api.models import Stock
from api.protos import database_pb2_grpc
from api.protos.database_pb2 import SymbolPair

import grpc

engine = create_engine('mysql+pymysql', 'root', 'admin', get_db_hostname(), '3306', 'mydb')

class DatabaseServer(database_pb2_grpc.DatabaseServicer):

    def __init__(self):
        pass

    def get_symbols(self, request, context):
        try:
            print(request)
            session = start_session(engine)
            arr = session.query(Stock).all()
            #print(arr)
            for item in arr:
                print(item.symbol, item.name)
                yield SymbolPair(symbol=item.symbol, name=item.name)
        except Exception as e:
            print(e)
            context.set_details(e)
            context.set_code(grpc.StatusCode.UNKNOWN)
            yield SymbolPair()
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

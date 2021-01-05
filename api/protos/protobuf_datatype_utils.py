import datetime

from google.protobuf.empty_pb2 import Empty as pb2_Empty
from google.protobuf.timestamp_pb2 import Timestamp as pb2_Timestamp

class Empty(pb2_Empty):

    def __init__(self):
        super.__init__()

class Timestamp(pb2_Timestamp):

    def __init__(self):
        super.__init__()

def datetime_to_timestamp(_datetime):
    # _datetime = datetime.datetime.now() - datetime.timedelta(days=180)
    timestamp = Timestamp()
    timestamp.FromDatetime(_datetime)
    return timestamp

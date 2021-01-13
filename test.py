import datetime
from datetime import date

from api.db import create_engine, start_session
from api.models import PttTrend, Stock, ReunionTrend
from api.utils import get_db_hostname

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql', 'root', 'admin', get_db_hostname(), '3306', 'mydb')
    session = start_session(engine)
    '''
    res = session.query(PttTrend, Stock).filter(PttTrend.symbol == Stock.symbol).filter(PttTrend.date >= datetime.datetime.strptime('05012021', "%d%m%Y").date()).all()
    for p, s in res:
        print(p, s)
    '''
    res = session.query(ReunionTrend).filter(
        ReunionTrend.date >= datetime.datetime.strptime('05012021', "%d%m%Y").date()).all()
    for p in res:
        print(p, p.stock)

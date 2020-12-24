import socket

from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy import create_engine as __create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import postgresql, mysql

from ..db import Base

def get_db_hostname():
    try:
        socket.gethostbyname('db')
        print(f'db hostname = db')
        return 'db'
    except Exception as e:
        print(f'gethostbyname(\'db\') failed: {e}')
        print(f'db hostname = localhost')
        return 'localhost'

def get_api_hostname():
    try:
        socket.gethostbyname('api')
        print(f'api hostname = api')
        return 'api'
    except Exception as e:
        print(f'gethostbyname(\'api\') failed: {e}')
        print(f'api hostname = localhost')
        return 'localhost'

def create_engine(adapter, user, password, host, port, database):
    create_engine.adapter = adapter
    print(f'==> create_engine for {create_engine.adapter}')
    try:
        return create_engine.engine
    except AttributeError:
        print('create new engine')
        create_engine.engine = __create_engine(f'{adapter}://{user}:{password}@{host}:{port}/{database}',
                                               pool_pre_ping=True,
                                               pool_recycle=3600*7)
        create_engine.engine.execute('SET GLOBAL max_allowed_packet=67108864;')
        return create_engine.engine

def create_all_tables_from_orm(engine):
    Base.metadata.create_all(engine)

def start_session(engine):
    print('==> start_session()')
    try:
        session = start_session.session_maker()
        session.execute("SELECT 1")
    except AttributeError:
        print('create new session maker')
        start_session.session_maker = sessionmaker()
        start_session.session_maker.configure(bind=engine)
        session = start_session.session_maker()
        session.execute('SELECT 1')
    return session

def compile_query(query):
    """from http://nicolascadou.com/blog/2014/01/printing-actual-sqlalchemy-queries"""
    compiler = query.compile if not hasattr(query, 'statement') else query.statement.compile
    if create_engine.adapter == 'mysql+pymysql':
        return compiler(dialect=mysql.dialect())
    else:
        return compiler(dialect=postgresql.dialect())

def insert(session, model, _dict):

    table = model.__table__

    stmt = mysql_insert(table).values(_dict)

    #print(compile_query(stmt))
    res = session.execute(stmt)
    print(f'{res.rowcount} row(s) matched')

def upsert(session, model, rows):

    table = model.__table__

    rowcount = 0

    if create_engine.adapter == 'mysql+pymysql':

        for row in rows:
            data_dict = {}
            for column, value in zip(table.c, row):
                data_dict[column.name] = value
            data_dict_wo_pk = dict(data_dict)
            for pk in list(table.primary_key.columns):
                del data_dict_wo_pk[pk.name]
            stmt = mysql_insert(table).values(data_dict)
            print(f'data_dict = {data_dict}, wo pk = {data_dict_wo_pk}')
            upsert_stmt = stmt.on_duplicate_key_update(data_dict_wo_pk)

            print(compile_query(upsert_stmt))
            res = session.execute(upsert_stmt)
            if res.rowcount != 0:
                rowcount += 1

        print(f'{rowcount} row(s) matched')
    else:
        stmt = postgres_insert(table).values(rows)

        update_cols = [
            c.name for c in table.c if c not in list(table.primary_key.columns)
        ]

        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=table.primary_key.columns,
            set_={
                k: getattr(stmt.excluded, k) for k in update_cols
            }
        )

        # print(compile_query(upsert_stmt))
        res = session.execute(upsert_stmt)
        print(f'{res.rowcount} row(s) matched')

    return rowcount
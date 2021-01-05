from api.db import create_engine, create_all_tables_from_orm, Base
from api.utils import get_db_hostname

if __name__ == '__main__':
    engine = create_engine('mysql+pymysql', 'root', 'admin', get_db_hostname(), '3306', 'mydb')
    # models should be imported,
    # so the class definitions would be executed,
    # and the models would be added into Base singleton
    from api.models import *
    for t in Base.metadata.sorted_tables:
        print(t.name)
    create_all_tables_from_orm(engine)

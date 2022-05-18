
MYSQL_DATA_HOST='127.0.0.1'
MYSQL_DATA_USER='root'
MYSQL_DATA_PASSWORD='Cathay168'
MYSQL_DATA_PORT=3306
MYSQL_DATA_DATABASE='Laptop'



from sqlalchemy import (
    create_engine,
    engine,
)


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{MYSQL_DATA_USER}:{MYSQL_DATA_PASSWORD}"
        f"@{MYSQL_DATA_HOST}:{MYSQL_DATA_PORT}/{MYSQL_DATA_DATABASE}"
    )
    print(address)
    engine = create_engine(address)
    connect = engine.connect()
    return connect

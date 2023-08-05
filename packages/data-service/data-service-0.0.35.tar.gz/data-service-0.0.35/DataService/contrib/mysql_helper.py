import pymysql

from app import config

cur_db_configs = config.cur_db_configs


_connect_dict = {}
connect_dict  = {}
for config in cur_db_configs:
    db = config["db"]
    _connect_dict[db] = config
    connect_dict[db] = pymysql.connect(**config)


def conn(db, verbose=False):
    try:
        connect_dict[db].ping()
        if verbose:
            print("use last connect...")
    except:
        if verbose:
            print("reconnect ~")
        connect_dict[db] = pymysql.connect(**_connect_dict[db])
    return connect_dict[db]


def get_data_from_mysql(sql: str, conn, verbose: bool=False) -> list:
    with conn:
        cursor = conn.cursor()
        if verbose:
            try:
                import sqlparse
                statment = sqlparse.format(sql, reindent=True, keyword_case="upper")
            except ImportError:
                statment = "execute: \n{}".format(sql)
            print(statment)
        cursor.execute(sql)

        columns = list(map(lambda obj: obj[0], cursor.description))
        data = cursor.fetchall()
        rets = [dict(zip(columns, ele)) for ele in data]
        return rets

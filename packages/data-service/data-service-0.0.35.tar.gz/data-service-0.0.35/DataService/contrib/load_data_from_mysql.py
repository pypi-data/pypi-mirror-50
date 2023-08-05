
import os
import time
import datetime
from concurrent.futures import (ThreadPoolExecutor, 
                                as_completed)

from apscheduler.schedulers.background import BackgroundScheduler

from app import config
from . import mysql_helper
from . import progressbar

WORKERS = 1
EXECUTOR = ThreadPoolExecutor(WORKERS)
EXPIRE = config.WebConfig.expire
VERBOSE = False
LAST_TIME = None
HOUR = config.WebConfig.hour
MINUTE = config.WebConfig.minute
SQL_DICT = config.sql_dict

CACHE = {}

def __load_data(kwargs):

    db = kwargs["db"]
    sql = kwargs["sql"]
    name = kwargs["name"]

    global CACHE

    conn = mysql_helper.conn(db)
    CACHE[name] = mysql_helper.get_data_from_mysql(sql, conn, verbose=VERBOSE)


def __load_data_all(sql_dict):
    rets = []
    kwarg_list = []
    for db, db_detail in sql_dict.items():
        for var_name, sql_name in db_detail.items():
            kwargs = {
                "db": db,
                "sql": config.parser.get(db, sql_name),
                "name": var_name
            }
            kwarg_list.append(kwargs)
            ret = EXECUTOR.submit(__load_data, kwargs)
            rets.append(ret)

    arg_nums = len(kwarg_list)

    start = start_ = time.perf_counter()
    for ret in as_completed(rets):
        end = time.perf_counter()
        progressbar.progressbar(len(CACHE), arg_nums,
                                min=0.5,
                                gap=5,
                                cur_consume_time=end-start,
                                total_consume_time=end-start_)
        start = time.perf_counter()
    print()


def load_data(sql_dict, force=False, message="", verbose=True):
    global LAST_TIME

    if LAST_TIME is None or force or not CACHE:
        if verbose:
            print(message)
        __load_data_all(sql_dict)
        LAST_TIME = time.perf_counter()
    else:
        cur_time = time.perf_counter()
        if cur_time - LAST_TIME > EXPIRE:
            if verbose:
                print("data expired, retrieve data......")
            __load_data(sql_dict)
        else:
            if verbose:
                print("use cache data".center(100, "*"))

# avoid second load when debug=True
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
  load_data(SQL_DICT)

kwargs = {"force": True,
          "message": "Time to restart"}

def restart_by_time():
    print("restart at: ", str(datetime.datetime.now()))
    load_data(sql_dict=SQL_DICT, **kwargs)


scheduler = BackgroundScheduler()
scheduler.add_job(restart_by_time, 'cron', hour=HOUR, minute=MINUTE)
scheduler.start()

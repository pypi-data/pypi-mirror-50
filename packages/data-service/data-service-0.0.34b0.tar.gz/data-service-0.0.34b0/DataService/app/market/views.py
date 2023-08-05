
import os
import datetime
from pprint import pprint
from collections import Counter

from flask import Blueprint, request

from . import model
from .. import decorators
from contrib import load_data_from_mysql
from contrib import date_helper
from contrib import load_dump_json


# ------------------------CONFIG-------------------------------------
DEBUG = True
url_prefix = None
json_dumps = decorators.json_dumps
cache = load_data_from_mysql.CACHE
print = pprint

DATA_PATH = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__))), 
        "data", 
        "global_cache.json"
    )

if os.path.exists(DATA_PATH):
    GLOBAL_CACHE = load_dump_json.load_json(DATA_PATH)
else:
    print("no path {}".format(DATA_PATH))
    GLOBAL_CACHE = {}
GLOBAL_CACHE["ACHIEVEMENT_EXPIRE"] = 60 * 60 * 2 # 2小时更新一次
# ------------------------CONFIG-------------------------------------

market_board = Blueprint(
        __name__, __name__,
        url_prefix=url_prefix,
    )


def test():
    return "hello, market"

market_board.add_url_rule("market/hello", 
    view_func=test, methods=["GET", "POST"])
market_board.add_url_rule("/market_board/hello", 
    view_func=test, methods=["GET", "POST"])

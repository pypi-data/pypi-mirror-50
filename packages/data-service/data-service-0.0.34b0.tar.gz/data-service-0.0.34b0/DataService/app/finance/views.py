import json
import datetime

from pprint import pprint
from collections import Counter
from functools import lru_cache

from flask import request, Blueprint

from . import model
from .. import decorators
from contrib import date_helper
from contrib import load_data_from_mysql


# ------------------------CONFIG-------------------------------------
DEBUG = True
url_prefix = None
json_dumps = decorators.json_dumps
cache = load_data_from_mysql.CACHE
print = pprint
# ------------------------CONFIG-------------------------------------

finance_board = Blueprint(
        __name__, __name__,
        url_prefix=url_prefix,
    )

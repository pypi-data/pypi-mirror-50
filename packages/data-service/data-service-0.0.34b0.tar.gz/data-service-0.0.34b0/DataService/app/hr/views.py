
import datetime
from pprint import pprint
from collections import Counter

from flask import Blueprint, jsonify, request

from . import model
from .. import decorators
from contrib import load_data_from_mysql
from contrib import date_helper

# ------------------------CONFIG-------------------------------------
DEBUG = True
url_prefix = None
json_dumps = decorators.json_dumps
cache = load_data_from_mysql.CACHE
print = pprint
# ------------------------CONFIG-------------------------------------

hr_board = Blueprint(
        __name__, __name__,
        url_prefix=url_prefix,
        )

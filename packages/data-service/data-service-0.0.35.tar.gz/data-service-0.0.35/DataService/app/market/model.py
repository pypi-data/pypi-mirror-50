import json
import copy
import time
import typing
import datetime

from functools import partial
from collections import defaultdict
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

import requests

from contrib import date_helper
from contrib import progressbar
from ..decorators import elapsed_time


parse_date = date_helper.parse_date
date_range = date_helper.date_range
progressbar = progressbar.progressbar
next_date_after_months = date_helper.next_date_after_months
Pool = ThreadPoolExecutor

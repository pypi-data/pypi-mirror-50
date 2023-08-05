
import json
import time
import datetime

from functools import wraps, singledispatch

from flask import jsonify

from .logger import logger
from contrib import json_encoder


def elapsed_time(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.info("%s 耗时：%ss", func.__name__, end-start)
        return result
    return wrap


def restful(code=200, message="success", **kw):
    def _wraps(func):
        @wraps(func)
        def __wraps__(*args, **kwargs):
            output = {}
            result = func(*args, **kwargs)
            result = json.loads(result)

            output["code"] = code
            output["message"] = message
            output["data"] = result
            if kw:
                output.update(kw)
            output = jsonify(output)
            return output
        return __wraps__
    return _wraps


@singledispatch
@restful()
def json_dumps():
    pass


@json_dumps.register(dict)
@restful()
def _(_rets: dict) -> dict:
    rets = {}
    for key, value in _rets.items():
        if isinstance(key, (datetime.date, datetime.datetime)):
            rets[str(key)[:10]] = value
        else:
            rets[key] = value
    return json.dumps(rets, ensure_ascii=False, 
                        cls=json_encoder.DecimalDateEncoder)


@json_dumps.register(list)
@restful()
def _(_rets: list) -> dict:
    return json.dumps(_rets, ensure_ascii=False,
            cls=json_encoder.DecimalDateEncoder)

import re
import copy
import typing
import datetime

from collections import defaultdict

import pendulum

from app.exceptions import DateFormatError


COMP = re.compile("(\d{4}).*?(\d{1,2}).*?(\d{1,2})")

def parse_date(date: str) -> typing.Optional[typing.Tuple[int]]:
    try:
        date = COMP.findall(date)
        if not date:
            raise DateFormatError("input format need: xxxx-xx-xx")
        date = tuple(map(int, date[0]))
        return date
    except:
        return


def date_range(start: str, end: str) -> list:
    start = parse_date(start)
    end = parse_date(end)

    start = datetime.date(*start)
    end = datetime.date(*end)

    days = (end - start).days
    if days < 0:
        raise ValueError("end must greater than start!")
    date_list = []
    for day in range(days+1):
        date = start + datetime.timedelta(day)
        date_list.append(date)
    return date_list


def timedelta(start: datetime.datetime, end: datetime.datetime) -> float:
    """
    calc timedelta
        unit: s
    """
    delta = end - start
    days = delta.days
    seconds = delta.seconds
    microseconds = delta.microseconds

    ret = days * 24 * 60 * 60 + seconds + microseconds/1e6
    return ret


date = typing.TypeVar("date", datetime.date, datetime.datetime)
def next_date_after_months(start: date, months: int) -> date:
    typ = type(start)
    if isinstance(start, (datetime.date, datetime.datetime)):
        start = str(start)[:10].split("-")
        end = pendulum.date(*map(int, start)).add(months=months)
        end = str(end)[:10].split("-")
        end = typ(*map(int, end))
        end = end - datetime.timedelta(days=1)
        return end
    raise TypeError("input must be datetime.date or datetime.datetime!")


def offer_start_end(end="today", delta=6, mode="day"):
    if end == "today":
        end = datetime.date.today()
    else:
        end = parse_date(end)
        end = datetime.date(*end)
    if mode == "day":
        start = end - datetime.timedelta(delta)
    elif mode == "month":
        start = next_date_after_months(end, delta)
    
    start = str(start)[:10]
    end = str(end)[:10]
    return start, end

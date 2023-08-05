import json
import decimal
import datetime


class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			return float(o)
		return super(DecimalEncoder, self).default(o)


class DateEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, datetime.date):
			return o.strftime("%Y-%m-%d")
		elif isinstance(o, datetime.datetime):
			return o.strftime("%Y-%m-%d %H:%M:%S")
		return super(DateEncoder, self).default(o)


class DecimalDateEncoder(DecimalEncoder, DateEncoder):
	"""转换日期、decimal为可json
	"""


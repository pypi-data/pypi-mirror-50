from flask import Blueprint

url_prefix = None

service_board = Blueprint(
        __name__, __name__,
        url_prefix=url_prefix,
    )

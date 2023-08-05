from imp import reload

from flask import request, Blueprint

from .. import decorators
from contrib import date_helper

url_prefix = None

ceo_board = Blueprint(
        __name__, __name__,
        url_prefix=url_prefix,
    )


@ceo_board.route("/ceo", methods=["GET", "POST"])
@decorators.elapsed_time
def ceo():
    return "hello, ceo"

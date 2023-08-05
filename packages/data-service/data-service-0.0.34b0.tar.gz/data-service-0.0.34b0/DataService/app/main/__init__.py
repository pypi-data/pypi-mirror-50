from ..ceo.views import ceo_board
from ..finance.views import finance_board
from ..hr.views import hr_board
from ..market.views import market_board
from ..service.views import service_board

blueprints = (
    ceo_board,
    finance_board,
    hr_board,
    market_board,
    service_board,
    )

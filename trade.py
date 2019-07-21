
import time


class InvalidTradeException(Exception):
    pass


class Trade(object):
    """
    Represents a trade (buy/sell) of any arbitrary stock. Would want to foreign key this to a stock if there was a DB
    """
    BUY_INDICATOR = "BUY"
    SELL_INDICATOR = "SELL"

    def __init__(self, timestamp, quantity, indicator, price):

        if timestamp > time.time():
            raise InvalidTradeException("Can't make a trade in the future!")

        if quantity <= 0:
            raise InvalidTradeException("Must trade 1 or more shares!")

        if indicator not in [self.BUY_INDICATOR, self.SELL_INDICATOR]:
            raise InvalidTradeException(f"Indicator {indicator} is not valid. "
                                        f"Must be {self.BUY_INDICATOR} or {self.SELL_INDICATOR}")

        if price <= 0:
            raise InvalidTradeException("Share price must be > 0!")

        self.timestamp = timestamp
        self.quantity = quantity
        self.indicator = indicator
        self.price = price

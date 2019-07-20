import unittest, time
from unittest import mock

from stocks import Stock
from trades import Trade, InvalidTradeException


class test_stock(unittest.TestCase):

    def setUp(self):
        self.stock_dividend_5 = Stock("TEST5", 5)
        self.stock_dividend_0 = Stock("TEST0", 0)

        trade_100_at_500 = Trade(time.time() - 60 , 100, Trade.BUY_INDICATOR, 500)
        trade_100_at_1000 = Trade(time.time() - 60, 100, Trade.BUY_INDICATOR, 1000)

        trade_100_at_100 = Trade(time.time() - 60 , 100, Trade.BUY_INDICATOR, 100)
        trade_100_at_105 = Trade(time.time() - 55, 100, Trade.SELL_INDICATOR, 105)
        trade_100_at_110 = Trade(time.time() - 50, 100, Trade.BUY_INDICATOR, 110)

        old_trade = Trade(time.time() - 10000, 999, Trade.BUY_INDICATOR, 1000)

        self.no_trades = []
        self.one_trade_at_500 = [trade_100_at_500]
        self.one_trade_at_500_and_old_trade = [old_trade, trade_100_at_500]
        self.three_trades = [trade_100_at_100, trade_100_at_105, trade_100_at_110]



    def test_calculate_price(self):

        # Base case, no trades
        self.stock_dividend_0.trades = self.no_trades
        self.assertEquals(self.stock_dividend_0.calculate_stock_price(), 0)

        # Easy case, one trade at 500
        self.stock_dividend_0.trades = self.one_trade_at_500
        self.assertEquals(self.stock_dividend_0.calculate_stock_price(), 500)

        # Old trades should get ignored
        self.stock_dividend_0.trades = self.one_trade_at_500_and_old_trade
        self.assertEquals(self.stock_dividend_0.calculate_stock_price(), 500)

        # Check that something resembling actual trades works
        self.stock_dividend_0.trades = self.three_trades

        expected_price = 105  # ((100*100)+(100*105)+(100*110)) / 300 = 105
        self.assertEquals(self.stock_dividend_0.calculate_stock_price(), expected_price)


    def test_dividend_yield(self):

        # If there are no trades, this will throw a div 0 error
        self.assertRaises(ZeroDivisionError, self.stock_dividend_0.calculate_dividend_yield)

        # Set the calculated price to 500 and test
        with mock.patch.object(Stock, 'calculate_stock_price', return_value=500):

            # common stock dividend 5, value = 500 yield = 0.01
            self.assertEquals(self.stock_dividend_5.calculate_dividend_yield(), 0.01)

            # common stock dividend 0
            self.assertEquals(self.stock_dividend_0.calculate_dividend_yield(), 0)


if __name__ == '__main__':
    unittest.main()
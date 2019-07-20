import unittest, time
from unittest import mock

from stocks import Stock, CommonStock, PreferredStock
from trades import Trade, InvalidTradeException


class test_stock(unittest.TestCase):

    def setUp(self):

        self.stock_dividend_5 = CommonStock("TEST5", 100, 5)
        self.stock_dividend_0 = CommonStock("TEST0", 100, 0)

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

        # Base case, no trades, returns par value
        self.stock_dividend_0.trades = self.no_trades
        self.assertEqual(self.stock_dividend_0.calculate_stock_price(), self.stock_dividend_0.par_value)

        # Easy case, one trade at 500
        self.stock_dividend_0.trades = self.one_trade_at_500
        self.assertEqual(self.stock_dividend_0.calculate_stock_price(), 500)

        # Old trades should get ignored
        self.stock_dividend_0.trades = self.one_trade_at_500_and_old_trade
        self.assertEqual(self.stock_dividend_0.calculate_stock_price(), 500)

        # Check that something resembling actual trades works
        self.stock_dividend_0.trades = self.three_trades

        expected_price = 105  # ((100*100)+(100*105)+(100*110)) / 300 = 105
        self.assertEqual(self.stock_dividend_0.calculate_stock_price(), expected_price)


    def test_dividend_yield(self):

        # Set the calculated price to 500 and test
        with mock.patch.object(Stock, 'calculate_stock_price', return_value=500):

            # common stock dividend 5, value = 500 yield = 0.01
            self.assertEqual(self.stock_dividend_5.calculate_dividend_yield(), 0.01)

            # common stock dividend 0
            self.assertEqual(self.stock_dividend_0.calculate_dividend_yield(), 0)

class test_preferred_stock(unittest.TestCase):
    """
    Preferred stocks have their own method of calculating dividend yield which differs from Common stocks.
    All other methods should be in common with CommonStocks
    """

    def setUp(self):
        self.stock_f_dividend_5 = PreferredStock("TEST5", 100, 0, 5)
        self.stock_f_dividend_0 = PreferredStock("TEST0", 100, 0, 0)

    def test_dividend_yield(self):

        # Set the calculated price to 100 for testing
        with mock.patch.object(PreferredStock, 'calculate_stock_price', return_value=100):

            # 0 fixed dividend = 0 yield
            self.assertEqual(self.stock_f_dividend_0.calculate_dividend_yield(), 0)

            # 5 fixed dividend * par value 100 / stock price 100 = 5 yield
            self.assertEqual(self.stock_f_dividend_5.calculate_dividend_yield(), 5)

if __name__ == '__main__':
    unittest.main()
import unittest, time
from unittest import mock

from exchange import Exchange


def quick_mock_stock(price):
    """
    Sets up a Mock to be used as a stand in for a stock

    :param int price: value to be returned from calculate_price
    :return:
    """
    stock = mock.Mock()
    stock.calculate_price.return_value = price
    return stock

class test_exchange(unittest.TestCase):
    """
    Test the Exchange object which handles transactions and exchange level info
    """

    def setUp(self):

        self.stock_100 = quick_mock_stock(100)
        self.stock_105 = quick_mock_stock(105)
        self.stock_110 = quick_mock_stock(110)
        self.stock_200 = quick_mock_stock(200)


    def test_all_share_index(self):
        """
        Test calculating the all share index
        """

        # basic test case, 1 stock of value 100, means the index value is 100
        exchange = Exchange([self.stock_100])
        all_share_index = exchange.calculate_all_share_index()

        self.assertEqual(all_share_index, 100)

        # Edge case, no stocks
        exchange = Exchange([])
        all_share_index = exchange.calculate_all_share_index()

        self.assertEqual(all_share_index, 0)

        # More realistic case, spread of stock values
        stocks = [self.stock_100, self.stock_105, self.stock_110, self.stock_200]
        exchange = Exchange(stocks)
        all_share_index = exchange.calculate_all_share_index()

        self.assertAlmostEqual(all_share_index, 123.283, places=3)  # note rounding.

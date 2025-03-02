import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pandas as pd
import os
from src.utils import (calculate_cashback, calculate_expenses, calculate_income,
                       get_currency_rates, get_stock_prices, main_page, events_page)


class TestFinanceFunctions(unittest.TestCase):

    def test_calculate_cashback(self):
        self.assertEqual(calculate_cashback(1000), 10)
        self.assertEqual(calculate_cashback(500), 5)
        with self.assertRaises(ValueError):
            calculate_cashback(-100)

    def test_calculate_expenses(self):
        data = {'type': ['expense', 'expense', 'income'], 'amount': [100, 200, 300], 'category': ['food', 'transport', 'salary']}
        df = pd.DataFrame(data)
        result = calculate_expenses(df)
        self.assertEqual(result['total_amount'], 300)
        self.assertEqual(len(result['main']), 2)

    def test_calculate_income(self):
        data = {'type': ['income', 'income', 'expense'], 'amount': [400, 500, 100], 'category': ['bonus', 'salary', 'food']}
        df = pd.DataFrame(data)
        result = calculate_income(df)
        self.assertEqual(result['total_amount'], 900)
        self.assertEqual(len(result['main']), 2)

    def test_get_currency_rates(self):
        rates = get_currency_rates()
        self.assertEqual(len(rates), 2)
        self.assertEqual(rates[0]['currency'], 'USD')

    @patch('src.utils.os.getenv')
    def test_get_stock_prices(self, mock_getenv):
        mock_getenv.return_value = 'fake_api_key'
        prices = get_stock_prices('fake_api_key')
        self.assertEqual(len(prices), 5)
        self.assertEqual(prices[0]['stock'], 'AAPL')

    def test_main_page(self):
        result = main_page('2021-12-21 12:00:00')
        self.assertIn('greeting', result)
        self.assertIn('cards', result)
        self.assertIn('top_transactions', result)

    @patch('src.utils.pd.DataFrame')
    @patch('src.utils.os.getenv')
    def test_events_page(self, mock_getenv, mock_df):
        mock_getenv.return_value = 'fake_api_key'
        mock_df_instance = MagicMock()
        mock_df.return_value = mock_df_instance

        # Настройка моков для фильтрации данных
        mock_df_instance.__getitem__.return_value = MagicMock()
        mock_df_instance.__getitem__.return_value.__ge__.return_value = MagicMock()
        mock_df_instance.__getitem__.return_value.__le__.return_value = MagicMock()
        mock_df_instance.__getitem__.return_value.__and__.return_value = MagicMock()

        result = events_page(mock_df_instance, '2021-12-21', 'M')
        self.assertIn('expenses', result)
        self.assertIn('income', result)


if __name__ == '__main__':
    unittest.main()
import pytest
from unittest.mock import patch
import pandas as pd
from src.views import main_page, events_page


@pytest.fixture
def mock_get_currency_rates():
    with patch('src.views.get_currency_rates', return_value=[{"currency": "USD", "rate": 73.45}]):
        yield


@pytest.fixture
def mock_get_stock_prices():
    with patch('src.views.get_stock_prices', return_value=[{"stock": "AAPL", "price": 150.00}]):
        yield


@pytest.mark.parametrize("date_time, expected_greeting", [
    ("2023-10-01 08:00:00", "Доброе утро!"),
    ("2023-10-01 18:00:00", "Добрый вечер!"),
])
def test_main_page(date_time, expected_greeting, mock_get_currency_rates, mock_get_stock_prices):
    result = main_page(date_time)
    assert result["greeting"] == expected_greeting
    assert len(result["cards"]) == 2
    assert result["cards"][0]["cashback"] == 12.62
    assert result["cards"][1]["cashback"] == 0.0794


@pytest.fixture
def sample_data():
    data = {
        'date': pd.date_range(start='2023-01-01', periods=10, freq='D'),
        'type': ['expense'] * 5 + ['income'] * 5,
        'amount': [100, 200, 150, 300, 250, 400, 500, 600, 700, 800],
        'category': ['food', 'transport', 'entertainment', 'food', 'other',
                     'salary', 'bonus', 'investment', 'salary', 'other']
    }
    return pd.DataFrame(data)


def test_events_page(sample_data):
    result = events_page(sample_data, '2023-01-05')
    assert "expenses" in result
    assert "income" in result
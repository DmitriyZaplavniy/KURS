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

@patch('src.utils.calculate_expenses')
@patch('src.utils.calculate_income')
def test_events_page(mock_calculate_income, mock_calculate_expenses, sample_data):
    # Настраиваем моки для возвращаемых значений
    mock_calculate_expenses.return_value = sample_data[sample_data['type'] == 'expense']
    mock_calculate_income.return_value = sample_data[sample_data['type'] == 'income']

    # Вызов функции
    result = events_page(sample_data, '2023-01-05')

    # Проверяем наличие ключей в результате
    assert "expenses" in result
    assert "income" in result

    # Проверяем значения расходов
    assert len(result["expenses"]) == 5  # Должно быть 5 записей расходов
    assert sum(item['amount'] for item in result["expenses"]) == 1000  # Сумма всех расходов

    # Проверяем значения доходов
    assert len(result["income"]) == 5  # Должно быть 5 записей доходов
    assert sum(item['amount'] for item in result["income"]) == 3000  # Сумма всех доходов

@patch('src.utils.calculate_expenses')
@patch('src.utils.calculate_income')
def test_events_page_no_data(mock_calculate_income, mock_calculate_expenses):
    # Настраиваем моки для возвращаемых значений
    mock_calculate_expenses.return_value = pd.DataFrame(columns=['date', 'type', 'amount', 'category'])
    mock_calculate_income.return_value = pd.DataFrame(columns=['date', 'type', 'amount', 'category'])

    # Вызов функции
    result = events_page(pd.DataFrame(), '2023-01-05')

    # Проверяем, что в результате есть ошибка
    assert "error" in result
    assert result["error"] == "DataFrame пуст."

from unittest.mock import patch
import pytest

@patch('src.utils.calculate_expenses')
@patch('src.utils.calculate_income')
def test_events_page_with_error(mock_calculate_income, mock_calculate_expenses):
    # Настраиваем моки для выбрасывания исключений
    mock_calculate_expenses.side_effect = Exception("Ошибка при расчете расходов")
    mock_calculate_income.side_effect = Exception("Ошибка при расчете доходов")

    # Вызов функции
    result = events_page(pd.DataFrame(), '2023-01-05')

    # Проверяем, что в результате есть ошибка
    assert "error" in result
    assert result["error"] == "Ошибка при расчете расходов"

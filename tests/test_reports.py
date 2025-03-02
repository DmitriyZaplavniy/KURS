import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.fixture
def sample_transactions():
    data = {
        'date': [datetime.now() - timedelta(days=i) for i in range(100)],
        'category': ['food'] * 50 + ['transport'] * 50,
        'amount': [10] * 50 + [20] * 50
    }
    return pd.DataFrame(data)


def test_spending_by_category(sample_transactions):
    result = spending_by_category(sample_transactions, 'food')
    assert not result.empty
    assert all(result['category'] == 'food')


def test_spending_by_weekday(sample_transactions):
    result = spending_by_weekday(sample_transactions)
    assert not result.empty
    assert len(result) == 7


def test_spending_by_workday(sample_transactions):
    result = spending_by_workday(sample_transactions)
    assert not result.empty
    assert len(result) == 2


@patch('src.reports.pd.DataFrame.to_json')  # Мокируем метод to_json
def test_spending_by_category_with_mock(mock_to_json, sample_transactions):
    # Настраиваем мок для to_json
    mock_to_json.return_value = None

    # Вызываем функцию
    result = spending_by_category(sample_transactions, 'food')

    # Проверяем, что мок был вызван
    mock_to_json.assert_called_once()
    assert not result.empty
    assert all(result['category'] == 'food')


@patch('src.reports.pd.DataFrame.to_json')  # Мокируем метод to_json
def test_spending_by_weekday_with_mock(mock_to_json, sample_transactions):
    # Настраиваем мок для to_json
    mock_to_json.return_value = None

    # Вызываем функцию
    result = spending_by_weekday(sample_transactions)

    # Проверяем, что мок был вызван
    mock_to_json.assert_called_once()
    assert not result.empty
    assert len(result) == 7


@patch('src.reports.pd.DataFrame.to_json')  # Мокируем метод to_json
def test_spending_by_workday_with_mock(mock_to_json, sample_transactions):
    # Настраиваем мок для to_json
    mock_to_json.return_value = None

    # Вызываем функцию
    result = spending_by_workday(sample_transactions)

    # Проверяем, что мок был вызван
    mock_to_json.assert_called_once()
    assert not result.empty
    assert len(result) == 2
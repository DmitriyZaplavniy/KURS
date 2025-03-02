import json
import pytest
from unittest.mock import patch
from src.services import analyze_cashback, investment_bank, simple_search, search_phone_numbers, search_person_transfers

@pytest.fixture
def sample_transactions():
    return [
        {"Дата операции": "2023-10-01", "Категория": "Супермаркеты", "Кешбэк": 100, "Описание": "Покупка в магазине"},
        {"Дата операции": "2023-10-02", "Категория": "Рестораны", "Кешбэк": 200, "Описание": "Ужин в ресторане"},
        {"Дата операции": "2023-10-01", "Категория": "Переводы", "Описание": "Перевод Алисе"},
        {"Дата операции": "2023-10-03", "Категория": "Переводы", "Описание": "+7 123 456-78-90"},
    ]

def test_analyze_cashback(sample_transactions):
    result = analyze_cashback(sample_transactions, 2023, 10)
    expected = {
        "Супермаркеты": 100,
        "Рестораны": 200
    }
    assert json.loads(result) == expected

def test_investment_bank(sample_transactions):
    result = investment_bank("2023-10", sample_transactions, 50)
    assert result == 0.0  # Ожидаемая сумма для инвесткопилки (нет операций с суммой >= 50)

@pytest.mark.parametrize("query, expected_count", [
    ("магазин", 1),
    ("ресторан", 1),
    ("перевод", 2),
])
def test_simple_search(sample_transactions, query, expected_count):
    result = simple_search(query, sample_transactions)
    assert len(json.loads(result)) == expected_count

def test_search_phone_numbers(sample_transactions):
    result = search_phone_numbers(sample_transactions)
    assert len(json.loads(result)) == 1  # Ожидаем одну транзакцию с номером телефона

def test_search_person_transfers(sample_transactions):
    result = search_person_transfers(sample_transactions)
    assert len(json.loads(result)) == 1  # Ожидаем одну транзакцию перевода физлицам
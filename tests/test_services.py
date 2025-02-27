import pytest
from src.services import analyze_cashback, investment_bank, simple_search, search_phone_numbers, search_person_transfers

def test_analyze_cashback():
    data = [
        {"Дата операции": "2023-10-01", "Категория": "Супермаркеты", "Кешбэк": 100},
        {"Дата операции": "2023-10-02", "Категория": "Рестораны", "Кешбэк": 200},
    ]
    result = analyze_cashback(data, 2023, 10)
    assert '"Супермаркеты": 100' in result
    assert '"Рестораны": 200' in result

def test_investment_bank():
    transactions = [
        {"Дата операции": "2023-10-01", "Сумма операции": 1712},
        {"Дата операции": "2023-10-02", "Сумма операции": 2000},
    ]
    result = investment_bank("2023-10", transactions, 50)
    assert result == 88.0

# Добавьте остальные тесты по аналогии
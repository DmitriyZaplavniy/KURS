from services import analyze_cashback, investment_bank, simple_search, search_phone_numbers, search_person_transfers
import pandas as pd
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
if __name__ == "__main__":
    # Пример данных
    transactions = [
        {"Дата операции": "2023-10-01", "Категория": "Супермаркеты", "Кешбэк": 100, "Сумма операции": 1000, "Описание": "Покупка в магазине"},
        {"Дата операции": "2023-10-02", "Категория": "Рестораны", "Кешбэк": 200, "Сумма операции": 2000, "Описание": "Ужин в ресторане"},
    ]

    # Пример использования сервисов
    print(analyze_cashback(transactions, 2023, 10))
    print(investment_bank("2023-10", transactions, 50))
    print(simple_search("Супермаркеты", transactions))
    print(search_phone_numbers(transactions))
    print(search_person_transfers(transactions))

if __name__ == "__main__":
    # Пример данных
    data = {
        'date': pd.date_range(start='1/1/2022', periods=100, freq='D'),
        'category': ['food'] * 50 + ['transport'] * 50,
        'amount': [10] * 50 + [20] * 50
    }
    df = pd.DataFrame(data)

    # Генерация отчетов
    spending_by_category(df, 'food')
    spending_by_weekday(df)
    spending_by_workday(df)
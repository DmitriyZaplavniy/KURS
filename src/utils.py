import os
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv
import pandas as pd
import json
import logging

# Загружаем переменные окружения из файла .env
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def get_greeting(current_time: str) -> str:
    """Определяет приветствие в зависимости от времени суток."""
    hour = int(current_time.split(':')[0])
    if 5 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 24:
        return "Добрый вечер!"
    else:
        return "Доброй ночи"


def calculate_cashback(total_spent: float) -> float:
    """Вычисляет кешбэк на основе потраченной суммы."""
    if total_spent < 0:
        raise ValueError("Сумма потраченных средств не может быть отрицательной.")
    return total_spent / 100


def calculate_expenses(dataframe: pd.DataFrame) -> Dict[str, Any]:
    """Вычисляет расходы по категориям."""
    expenses = dataframe[dataframe['type'] == 'expense']
    total_expenses = expenses['amount'].sum()

    # Основные категории
    main_expenses = expenses.groupby('category')['amount'].sum().nlargest(7).reset_index()

    # Остальные расходы
    other_expenses_amount = total_expenses - main_expenses['amount'].sum()
    if other_expenses_amount > 0:
        other_expenses = pd.DataFrame({'category': ['Остальное'], 'amount': [other_expenses_amount]})
        main_expenses = pd.concat([main_expenses, other_expenses], ignore_index=True)

    # Переводы и наличные
    transfers_and_cash = expenses[expenses['category'].isin(['Наличные', 'Переводы'])].groupby('category')[
        'amount'].sum().reset_index()

    return {
        "total_amount": round(total_expenses),
        "main": main_expenses.to_dict(orient='records'),
        "transfers_and_cash": transfers_and_cash.to_dict(orient='records')
    }


def calculate_income(dataframe: pd.DataFrame) -> Dict[str, Any]:
    """Вычисляет доходы по категориям."""
    income = dataframe[dataframe['type'] == 'income']
    total_income = income['amount'].sum()

    # Основные категории
    main_income = income.groupby('category')['amount'].sum().nlargest(7).reset_index()

    return {
        "total_amount": round(total_income),
        "main": main_income.to_dict(orient='records')
    }


def get_currency_rates() -> List[Dict[str, Any]]:
    """Возвращает курсы валют."""
    return [
        {"currency": "USD", "rate": 73.21},
        {"currency": "EUR", "rate": 87.08}
    ]


def get_stock_prices(api_key: str, symbol: str = "AAPL") -> List[Dict[str, Any]]:
    """Возвращает цены на акции."""
    # Заглушка для получения цен акций (можно использовать API)
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08}
    ]


def main_page(date_time: str) -> Dict[str, Any]:
    """Функция для страницы «Главная»."""
    current_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
    greeting = get_greeting(current_time)

    # Пример данных о картах и транзакциях
    cards = [
        {"last_digits": "5814", "total_spent": 1262.00},
        {"last_digits": "7512", "total_spent": 7.94}
    ]

    for card in cards:
        card["cashback"] = calculate_cashback(card["total_spent"])

    top_transactions = [
        {"date": "21.12.2021", "amount": 1198.23, "category": "Переводы",
         "description": "Перевод Кредитная карта. ТП 10.2 RUR"},
        {"date": "20.12.2021", "amount": 829.00, "category": "Супермаркеты", "description": "Лента"},
        {"date": "20.12.2021", "amount": 421.00, "category": "Различные товары", "description": "Ozon.ru"},
        {"date": "16.12.2021", "amount": -14216.42, "category": "ЖКХ", "description": "ЖКУ Квартира"},
        {"date": "16.12.2021", "amount": 453.00, "category": "Бонусы", "description": "Кешбэк за обычные покупки"}
    ]

    currency_rates = get_currency_rates()

    # Получаем API-ключ из окружения
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY не установлен в переменных окружения.")

    # Получаем цены на акции
    stock_prices = get_stock_prices(api_key, "AAPL")  # Пример для акции AAPL

    return {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }


def events_page(dataframe: pd.DataFrame, date_str: str, range_option: str = 'M') -> str:
    """Функция для страницы «События»."""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # Определение диапазона данных
        if range_option == 'W':
            start_date = date - pd.DateOffset(days=date.weekday())
            end_date = start_date + pd.DateOffset(days=6)
        elif range_option == 'M':
            start_date = date.replace(day=1)
            end_date = date
        elif range_option == 'Y':
            start_date = date.replace(month=1, day=1)
            end_date = date
        elif range_option == 'ALL':
            start_date = pd.Timestamp.min
            end_date = date
        else:
            logging.error("Invalid range option provided.")
            return json.dumps({"error": "Invalid range option."})

        # Фильтрация данных по дате
        filtered_data = dataframe[(dataframe['date'] >= start_date) & (dataframe['date'] <= end_date)]

        # Расчет расходов и поступлений
        expenses_data = calculate_expenses(filtered_data)
        income_data = calculate_income(filtered_data)

        # Получение курса валют и цен акций
        currency_rates = get_currency_rates()

        # Получение API_KEY из переменных окружения
        api_key = os.getenv("API_KEY")
        if not api_key:
            logging.error("API_KEY not found in environment variables.")
            return json.dumps({"error": "API_KEY not found."})

        stock_prices = get_stock_prices(api_key)

        # Формирование JSON-ответа
        response = {
            "expenses": expenses_data,
            "income": income_data,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices
        }

        return json.dumps(response, ensure_ascii=False)

    except Exception as e:
        logging.error(f"Ошибка в events_page: {e}")
        return json.dumps({"error": str(e)})



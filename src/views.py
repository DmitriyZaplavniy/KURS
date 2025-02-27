import os
from datetime import datetime
from typing import Dict, Any
from src.api import get_currency_rates, get_stock_prices
from .utils import get_greeting, calculate_cashback
from dotenv import load_dotenv
from src.utils import calculate_expenses, calculate_income, get_currency_rates, get_stock_prices
import pandas as pd
from datetime import datetime
import json
import logging

# Загружаем переменные окружения из файла .env
load_dotenv()

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


# Настройка логирования
logging.basicConfig(level=logging.INFO)

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
        stock_prices = get_stock_prices(os.getenv("API_KEY"))  # Передача api_key

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



import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import re

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_cashback(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """
    Анализирует выгодные категории для повышенного кешбэка за указанный месяц и год.

    :param data: Список транзакций.
    :param year: Год для анализа.
    :param month: Месяц для анализа.
    :return: JSON с анализом кешбэка по категориям.
    """
    cashback_by_category = {}
    for transaction in data:
        date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')
        if date.year == year and date.month == month:
            category = transaction['Категория']
            cashback = transaction.get('Кешбэк', 0)
            if category in cashback_by_category:
                cashback_by_category[category] += cashback
            else:
                cashback_by_category[category] = cashback

    logging.info(f"Анализ кешбэка за {month}/{year} завершен.")
    return json.dumps(cashback_by_category, ensure_ascii=False, indent=4)

def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которую можно отложить в «Инвесткопилку» за указанный месяц.

    :param month: Месяц для расчета (формат 'YYYY-MM').
    :param transactions: Список транзакций.
    :param limit: Предел округления.
    :return: Сумма для «Инвесткопилки».
    """
    total_investment = 0.0
    for transaction in transactions:
        date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')
        if date.strftime('%Y-%m') == month:
            amount = transaction['Сумма операции']
            rounded_amount = (amount // limit + 1) * limit
            investment = rounded_amount - amount
            total_investment += investment

    logging.info(f"Сумма для «Инвесткопилки» за {month}: {total_investment}.")
    return total_investment

def simple_search(query: str, transactions: List[Dict[str, Any]]) -> str:
    """
    Поиск транзакций по строке запроса.

    :param query: Строка для поиска.
    :param transactions: Список транзакций.
    :return: JSON с результатами поиска.
    """
    results = [t for t in transactions if query.lower() in t['Описание'].lower() or query.lower() in t['Категория'].lower()]
    logging.info(f"Найдено {len(results)} транзакций по запросу '{query}'.")
    return json.dumps(results, ensure_ascii=False, indent=4)

def search_phone_numbers(transactions: List[Dict[str, Any]]) -> str:
    """
    Поиск транзакций, содержащих мобильные номера в описании.

    :param transactions: Список транзакций.
    :return: JSON с результатами поиска.
    """
    phone_pattern = re.compile(r'\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2}')
    results = [t for t in transactions if phone_pattern.search(t['Описание'])]
    logging.info(f"Найдено {len(results)} транзакций с мобильными номерами.")
    return json.dumps(results, ensure_ascii=False, indent=4)

def search_person_transfers(transactions: List[Dict[str, Any]]) -> str:
    """
    Поиск транзакций, относящихся к переводам физлицам.

    :param transactions: Список транзакций.
    :return: JSON с результатами поиска.
    """
    name_pattern = re.compile(r'[А-Я][а-я]+\s[А-Я]\.')
    results = [t for t in transactions if t['Категория'] == 'Переводы' and name_pattern.search(t['Описание'])]
    logging.info(f"Найдено {len(results)} транзакций переводов физлицам.")
    return json.dumps(results, ensure_ascii=False, indent=4)
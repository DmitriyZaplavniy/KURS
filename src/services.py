import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import re

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_cashback(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """
    Анализирует кешбэк по категориям за указанный месяц и год.

    :param data: Список транзакций.
    :param year: Год для анализа.
    :param month: Месяц для анализа.
    :return: JSON с кешбэком по категориям.
    """
    cashback_by_category = {}
    for transaction in data:
        try:
            date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')
            if date.year == year and date.month == month:
                category = transaction['Категория']
                cashback = transaction.get('Кешбэк', 0)
                if cashback > 0:  # Учитываем только положительный кешбэк
                    cashback_by_category[category] = cashback_by_category.get(category, 0) + cashback
        except KeyError as e:
            logging.warning(f"Отсутствует ключ в транзакции: {e}")

    logging.info(f"Анализ кешбэка за {month}/{year} завершен.")
    return json.dumps(cashback_by_category, ensure_ascii=False, indent=4)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму для инвесткопилки за указанный месяц.

    :param month: Месяц в формате 'YYYY-MM'.
    :param transactions: Список транзакций.
    :param limit: Лимит для округления.
    :return: Сумма для инвесткопилки.
    """
    total_investment = 0.0
    for transaction in transactions:
        try:
            date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')
            if date.strftime('%Y-%m') == month:
                amount = transaction.get('Сумма операции', 0)
                if amount > 0:  # Учитываем только положительные суммы
                    investment = (amount // limit) * limit
                    total_investment += investment
        except KeyError as e:
            logging.warning(f"Отсутствует ключ в транзакции: {e}")

    logging.info(f"Сумма для инвесткопилки за {month}: {total_investment}")
    return total_investment


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> str:
    """
    Поиск транзакций по строке запроса.

    :param query: Строка для поиска.
    :param transactions: Список транзакций.
    :return: JSON с результатами поиска.
    """
    results = [
        t for t in transactions
        if query.lower() in t.get('Описание', '').lower() or query.lower() in t.get('Категория', '').lower()
    ]
    logging.info(f"Найдено {len(results)} транзакций по запросу '{query}'.")
    return json.dumps(results, ensure_ascii=False, indent=4)


def search_phone_numbers(transactions: List[Dict[str, Any]]) -> str:
    """
    Поиск транзакций, содержащих мобильные номера в описании.

    :param transactions: Список транзакций.
    :return: JSON с результатами поиска.
    """
    phone_pattern = re.compile(r'\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2}')
    results = [t for t in transactions if phone_pattern.search(t.get('Описание', ''))]
    logging.info(f"Найдено {len(results)} транзакций с мобильными номерами.")
    return json.dumps(results, ensure_ascii=False, indent=4)


def search_person_transfers(transactions: List[Dict[str, Any]]) -> str:
    """
    Поиск переводов физлицам.

    :param transactions: Список транзакций.
    :return: JSON с результатами поиска.
    """
    name_pattern = re.compile(r'Перевод\s+[А-Я][а-я]+\s*[А-Я]?')  # Исправленное регулярное выражение
    results = [
        t for t in transactions
        if t.get('Категория') == 'Переводы' and name_pattern.search(t.get('Описание', ''))
    ]
    logging.info(f"Найдено {len(results)} переводов физлицам.")
    return json.dumps(results, ensure_ascii=False, indent=4)



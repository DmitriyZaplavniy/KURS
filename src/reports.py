import functools
import json
import pandas as pd
from typing import Optional, Callable
import logging
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def report_to_file(default_filename: str = "report.json"):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            filename = kwargs.get('filename', default_filename)
            with open(filename, 'w') as f:
                if isinstance(result, pd.DataFrame):
                    result.to_json(f, orient='records', lines=True)
                else:
                    json.dump(result, f, indent=4)
            logging.info(f"Report saved to {filename}")
            return result
        return wrapper
    return decorator

def report_to_file_with_name(filename: str):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, 'w') as f:
                if isinstance(result, pd.DataFrame):
                    result.to_json(f, orient='records', lines=True)
                else:
                    json.dump(result, f, indent=4)
            logging.info(f"Report saved to {filename}")
            return result
        return wrapper
    return decorator


@report_to_file()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    :param transactions: Датафрейм с транзакциями.
    :param category: Название категории.
    :param date: Дата отсчета (по умолчанию текущая дата).
    :return: Датафрейм с тратами по категории.
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y-%m-%d')

    three_months_ago = date - timedelta(days=90)
    filtered = transactions[(transactions['category'] == category) &
                            (transactions['date'] >= three_months_ago) &
                            (transactions['date'] <= date)]
    return filtered


@report_to_file()
def spending_by_weekday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в каждый из дней недели за последние три месяца.

    :param transactions: Датафрейм с транзакциями.
    :param date: Дата отсчета (по умолчанию текущая дата).
    :return: Датафрейм со средними тратами по дням недели.
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y-%m-%d')

    three_months_ago = date - timedelta(days=90)
    filtered = transactions[(transactions['date'] >= three_months_ago) &
                            (transactions['date'] <= date)]
    filtered['weekday'] = filtered['date'].dt.weekday
    return filtered.groupby('weekday')['amount'].mean().reset_index()


@report_to_file()
def spending_by_workday(transactions: pd.DataFrame,
                        date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочий и в выходной день за последние три месяца.

    :param transactions: Датафрейм с транзакциями.
    :param date: Дата отсчета (по умолчанию текущая дата).
    :return: Датафрейм со средними тратами в рабочий и выходной день.
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y-%m-%d')

    three_months_ago = date - timedelta(days=90)
    filtered = transactions[(transactions['date'] >= three_months_ago) &
                            (transactions['date'] <= date)]
    filtered['is_weekend'] = filtered['date'].dt.weekday >= 5
    return filtered.groupby('is_weekend')['amount'].mean().reset_index()
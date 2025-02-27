import requests
import logging
from typing import Dict

# Замените на ваши реальные API-ключи
EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
ALPHA_VANTAGE_API_KEY = 'ce33fc99a5d689c1a3a20247'
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

def get_currency_rates() -> dict:
    """Получает актуальные курсы валют."""
    response = requests.get(EXCHANGE_RATE_API_URL)
    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        return {"error": f"Не удалось получить курсы валют: {response.status_code}"}

def get_stock_prices(api_key: str, symbol: str) -> Dict[str, float]:
    """Возвращает текущие цены на акции."""
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}"
        response = requests.get(url)
        data = response.json()

        # Пример извлечения цены акции
        latest_time = list(data["Time Series (1min)"].keys())[0]
        price = data["Time Series (1min)"][latest_time]["1. open"]

        return {symbol: float(price)}
    except Exception as e:
        logging.error(f"Ошибка при получении цен на акции: {e}")
        return {}

# Пример использования функций
if __name__ == "__main__":  # Исправлено условие
    # Получаем курсы валют
    currency_rates = get_currency_rates()
    print("Курсы валют:", currency_rates)

    # Получаем цены акций
    stock_symbol = 'AAPL'  # Замените на нужный символ акции
    stock_data = get_stock_prices(ALPHA_VANTAGE_API_KEY, stock_symbol)
    print("Цены акций:", stock_data)

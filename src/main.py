import pandas as pd
from datetime import datetime
from src.reports import (
    spending_by_category,
    spending_by_weekday,
    spending_by_workday,
)

def main():
    # Загрузка данных из Excel
    df = pd.read_excel("data/operations.xlsx")

    # Текущая дата
    today = datetime.now().strftime("%Y-%m-%d")

    # Отчет: Траты по категории
    category_spending = spending_by_category(df, "Супермаркеты", today)
    print("Траты по категории 'Супермаркеты':")
    print(category_spending)

    # Отчет: Траты по дням недели
    weekday_spending = spending_by_weekday(df, today)
    print("Средние траты по дням недели:")
    print(weekday_spending)

    # Отчет: Траты в рабочий/выходной день
    workday_spending = spending_by_workday(df, today)
    print("Средние траты в рабочий/выходной день:")
    print(workday_spending)

if __name__ == "__main__":
    main()

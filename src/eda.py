"""
Неделя 1: инструменты для разведочного анализа (EDA).

explore() и churn_rate_by() уже написаны — применяйте их, переписывать не надо.
Ваша задача на неделе 1 — функция missing_months() внизу файла.
"""
import pandas as pd


def explore(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """ГОТОВО. Быстрый профиль таблицы: типы, пропуски, уникальные значения."""
    print(f"===== {name} =====")
    print(f"Размер: {df.shape[0]} строк, {df.shape[1]} столбцов")

    summary = pd.DataFrame({
        "тип": df.dtypes,
        "пропусков": df.isna().sum(),
        "пропусков_%": (df.isna().mean() * 100).round(1),
        "уникальных": df.nunique(),
    })
    print(summary)

    numeric = df.select_dtypes("number")
    if not numeric.empty:
        print("\n--- Числовые столбцы ---")
        print(numeric.describe().T.round(2))

    return summary


def churn_rate_by(df: pd.DataFrame, target_col: str, group_col: str) -> pd.DataFrame:
    """ГОТОВО. Доля оттока в разбивке по группе (сегмент/продукт/регион).

    Колонки target_col в данных нет — вы создаёте её сами, см. тетрадь 5.3, шаг 5.
    """
    return (
        df.groupby(group_col)[target_col]
        .agg(["mean", "count"])
        .rename(columns={"mean": "доля_оттока", "count": "клиентов"})
        .sort_values("доля_оттока", ascending=False)
    )


def missing_months(usage: pd.DataFrame) -> pd.DataFrame:
    """Дыры в помесячных данных клиента.

    Для каждого клиента: первый месяц, последний месяц, сколько месяцев
    фактически есть и сколько должно быть между первым и последним.

    Отсутствие месяцев В СЕРЕДИНЕ истории клиента — это дыра в данных,
    а не уход. Отличать одно от другого понадобится на неделе 2.

    Returns
    -------
    DataFrame с индексом client_id и столбцами:
        first_month, last_month, n_months_actual, n_months_expected, has_gap

    TODO (неделя 1)
    """
    raise NotImplementedError("Реализуйте на неделе 1")

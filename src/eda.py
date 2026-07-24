"""
Неделя 1: инструменты для разведочного анализа (EDA).
"""
import pandas as pd


def explore(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Быстрый профиль таблицы: типы, пропуски, уникальные значения.

    Parameters
    ----------
    df : исходная таблица
    name : имя таблицы для заголовка вывода

    Returns
    -------
    DataFrame со сводкой по столбцам (тип, % пропусков, число уникальных)
    """
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
    """Доля оттока в разбивке по группе (сегмент/продукт/регион).

    TODO (неделя 1): использовать для первой проверки гипотезы
    "отток зависит от сегмента".
    """
    return (
        df.groupby(group_col)[target_col]
        .agg(["mean", "count"])
        .rename(columns={"mean": "доля_оттока", "count": "клиентов"})
        .sort_values("доля_оттока", ascending=False)
    )

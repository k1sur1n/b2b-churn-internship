"""
Неделя 2-3: сборка обучающей выборки и построение признаков.

Правило №1 проекта: признаки строятся ТОЛЬКО из данных до точки отсчёта
(snapshot), таргет — ТОЛЬКО из данных после.

Что писать когда:
  неделя 2 — window_bounds, make_features (минимум, 4 признака), make_target, build_snapshot
  неделя 3 — расширить make_features до пяти групп признаков

Сигнатуры функций не меняйте — по ним ревьюер сравнивает решения.
"""
import numpy as np
import pandas as pd

# --- Параметры схемы. Общие для всего потока, менять нельзя. ---
OBSERVATION_MONTHS = 6   # окно наблюдения, включая сам месяц snapshot
GAP_MONTHS = 2           # слепой зазор: месяцы, которые не используются вообще
FORECAST_MONTHS = 3      # окно прогноза

SILENT_CHURN_RATIO = 0.20  # порог "тихого" оттока

SNAPSHOTS = ['2024-07', '2024-10', '2025-01', '2025-04',
             '2025-07', '2025-10', '2026-01']


def window_bounds(snapshot: str):
    """Границы окна наблюдения и окна прогноза.

    Для snapshot = '2025-01':
        окно наблюдения  2024-08 .. 2025-01   (снапшот входит сюда)
        слепой зазор     2025-02 .. 2025-03   (не используется вообще)
        окно прогноза    2025-04 .. 2025-06

    Returns
    -------
    (obs_start, obs_end, fc_start, fc_end) — строки вида 'YYYY-MM'

    TODO (неделя 2): реализовать через pd.Period, см. тетрадь 3.5
    """
    raise NotImplementedError("Реализуйте на неделе 2")


def make_features(obs: pd.DataFrame, obs_end) -> pd.DataFrame:
    """Строит признаки по данным окна наблюдения.

    Parameters
    ----------
    obs : помесячные данные ОКНА НАБЛЮДЕНИЯ (client_id, month, revenue, ...)
    obs_end : последний месяц окна наблюдения (он же snapshot)

    Returns
    -------
    DataFrame признаков с индексом client_id

    TODO (неделя 2) — минимальная версия, 4 признака:
        rev_mean          средний revenue за окно
        rev_last          revenue последнего месяца окна
        rev_last_to_mean  rev_last / rev_mean   (главный сигнал падения)
        n_months          сколько месяцев клиент присутствует в окне

    TODO (неделя 3) — расширить до пяти групп:
        платежи, динамика, объём отношений, сигналы боли, категориальные
    """
    raise NotImplementedError("Реализуйте на неделе 2 (минимум), расширьте на неделе 3")


def make_target(fut: pd.DataFrame, alive, rev_mean: pd.Series) -> pd.Series:
    """Таргет по окну прогноза.

    1, если выполняется хотя бы одно:
      (а) в окне прогноза у клиента нет ни одной строки  -> явное расторжение
      (б) средний revenue в окне прогноза < SILENT_CHURN_RATIO * rev_mean -> тихий уход

    ВНИМАНИЕ: клиентов из alive, которых нет в fut, потерять нельзя — это и есть
    отток. Выравнивайте по alive через reindex, а НЕ через inner join.

    TODO (неделя 2)
    """
    raise NotImplementedError("Реализуйте на неделе 2")


def build_snapshot(usage: pd.DataFrame, clients: pd.DataFrame, snapshot: str) -> pd.DataFrame:
    """Собирает обучающую выборку для одной точки отсчёта.

    Returns
    -------
    DataFrame: client_id | snapshot_date | признаки | segment | product | region | target

    TODO (неделя 2), шесть блоков:
      1. границы окон                       -> window_bounds()
      2. срез окна наблюдения               -> obs
      3. скоуп: живые на конец окна         -> alive ("мёртвые души", тетрадь 2.6)
      4. признаки только из obs             -> make_features()
      5. таргет только из окна прогноза     -> make_target()
      6. сборка + статичные атрибуты клиента (segment/product/region/tenure)
    """
    raise NotImplementedError("Реализуйте на неделе 2")


# --------------------------------------------------------------------------
# ГОТОВО — переписывать не нужно, просто применяйте
# --------------------------------------------------------------------------

def trend_slope(s: pd.Series) -> float:
    """Наклон линейного тренда: >0 растёт, <0 падает."""
    y = s.to_numpy(dtype=float)
    if len(y) < 2:
        return 0.0
    x = np.arange(len(y))
    return float(np.polyfit(x, y, 1)[0])


def months_declining(s: pd.Series) -> int:
    """Сколько последних месяцев подряд значение снижалось."""
    diffs = s.diff().to_numpy()[1:]
    cnt = 0
    for d in diffs[::-1]:
        if d < 0:
            cnt += 1
        else:
            break
    return cnt

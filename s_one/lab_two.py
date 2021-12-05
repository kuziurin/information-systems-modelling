"""
Смоделировать информационный поток из 200 событий.
Интервалы времени между наступлением событий распределены по закону распределения
вероятностей из лабораторной работы.

Вывести значения интервалов времени между соседними событиями и моменты наступления
событий. Произвести оценку качества моделирования с помощью критерия X^2 по аналогии с
лабораторной работой. Параметры для расчета критерия взять из лабораторной работы.

Закон Рэлея.

a = сигма^2 = 1.
"""
from pprint import pprint
from typing import List, Tuple

import pandas as pd

from lab_one import get_random_nums


NUMBERS_COUNT = 200


EventTimes = List[Tuple[int, float, float]]


def show_result_dataframe(events_times: EventTimes) -> None:
    """Сформировать и отобразить dataframe соответствия моментов наступления событий и
    дельт времени.

    Args:
        events_times: Список кортежей (индекс, дельта времени, момент времени)
    """
    df = pd.DataFrame(events_times, columns=["index", "time_delta", "event_time"])
    print(df)


def show_result_table(events_times: EventTimes) -> None:
    """Отобразить таблицу соответствия моментов наступления событий и дельт времени.

    Args:
        events_times: Список кортежей (индекс, дельта времени, момент времени)
    """
    print("  index  time_delta  event_time")
    pprint(events_times)


def get_event_times(delta_values: List[float]) -> EventTimes:
    """Получить значения моментов наступления событий и соответствующих интервалов
    времени.

    Args:
        delta_values: Список значений дельт времени.

    Returns:
        Список кортежей (индекс, дельта времени, момент времени)
    """
    event_time = 0
    idx = 0
    delta_values.insert(0, 0)
    event_times = []
    for time_delta in delta_values:
        event_time += time_delta
        event_times.append((idx, time_delta, event_time))
        idx += 1

    return event_times


def main():
    events_times = get_event_times(get_random_nums(NUMBERS_COUNT))
    # show_result_dataframe(events_times)
    show_result_table(events_times)


if __name__ == "__main__":
    main()

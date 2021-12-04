"""
Получить последовательность из N=1000 реализаций случайной величины x, распределенной
по закону Рэлея.

a = сигма^2 = 1.
"""

import math
from collections import defaultdict
from pprint import pprint
from random import random
from typing import Any, Dict, List

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


NUMBERS_COUNT = 1000  # Количество случайных чисел.
RANGES_COUNT = 12  # Количество интервалов (групп распределения).


def get_random_nums(count: int) -> List[float]:
    """Получить случайные числа."""
    return [math.sqrt(-2 * math.log(1 - random())) for _ in range(count)]


def get_p_stat(ranges: Dict[int, Any], k: int, range_delta: float) -> float:
    """Получить статистическую вероятность попадания случайной величины в интервал."""
    return (ranges[k]["count"] / 1000) / range_delta


def get_p_theor(x: float) -> float:
    """Получить теоретическую вероятность попадания случайной величины в интервал."""
    return x * math.exp((-(x ** 2)) / 2)


def get_x_squared(ranges: Dict, n: int) -> float:
    """Получить X^2."""
    return sum(
        ((ranges[k]["count"] / NUMBERS_COUNT) - ranges[k]["p_theor"])
        ** 2 / ranges[k]["p_theor"]
        for k in range(1, n + 1)
    )


def get_ranges(nums: List[float], ranges_count: int) -> None:
    """Получить распределение по ranges_count группам (интервалам).

    Note:
        По итогу вычислений выводится гистограмма и графики соответствия статистической
        и теоретической плотностей. График статистической плотности соответствует
        гистограмме.

    Args:
        nums: Список чисел.
        ranges_count: Количество групп распределения.

    """
    min_value = min(nums)
    max_value = max(nums)
    range_delta = (max_value - min_value) / ranges_count
    boundaries = [min_value + range_delta * count for count in range(ranges_count + 1)]

    pprint(f"{min_value=}")
    pprint(f"{max_value=}")
    print("\nBoundaries (Xmin...Xmax):")
    pprint(boundaries)
    print()

    ranges = defaultdict(dict)

    # ranges = [1...12]
    for idx in range(1, ranges_count + 1):
        ranges[idx]["count"] = 0

    for num in nums:
        for idx in range(1, ranges_count + 1):
            if num < boundaries[idx]:
                ranges[idx]["count"] += 1
                break

    for k, v in ranges.copy().items():
        # Get p_stat
        ranges[k]["p_stat"] = v["count"] / NUMBERS_COUNT / range_delta

        if k <= 12:
            # Boundaries indexes = [0...12]
            x = (boundaries[k - 1] + boundaries[k]) / 2
            # Get x_avg
            ranges[k]["x_avg"] = x
            # Get p_theor
            ranges[k]["p_theor"] = get_p_theor(x)

    df_full = pd.DataFrame([{**v} for v in ranges.values()])
    pprint(df_full)

    print(f"Numbers count: {len(nums)}")
    print(f"Counters sum: {sum(v['count'] for v in ranges.values())}")

    # Get X^2
    x_squared = get_x_squared(ranges, ranges_count)
    print(f"X^2: {x_squared}\nCorrect: {x_squared <= 24.7}\n")

    # Plot with Seaborn
    df = pd.DataFrame.from_dict({"nums": get_random_nums(NUMBERS_COUNT)})
    sns.barplot(x=df_full["x_avg"], y=df_full["p_stat"])
    plt.show()

    # Plot with Matplotlib
    plt.plot(df_full["x_avg"], df_full["p_theor"], color="red")
    plt.plot(df_full["x_avg"], df_full["p_stat"], color="blue")
    plt.show()


def main():
    get_ranges(get_random_nums(NUMBERS_COUNT), RANGES_COUNT)


if __name__ == "__main__":
    main()

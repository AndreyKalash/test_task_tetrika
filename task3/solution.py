def intervals_to_sessions(intervals: list[int]) -> list[tuple[int, int]]:
    """Преобразует список вида [t0_start, t0_end, t1_start, t1_end, ...] в список кортежей [(t0_start, t0_end), ...]."""
    return [(intervals[i], intervals[i + 1]) for i in range(0, len(intervals), 2)]


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Сливает пересекающиеся или соприкасающиеся интервалы в один."""
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        # получаем последний интервал
        last_start, last_end = merged[-1]
        # если есть пересечение - объединяем интервалы
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def intersect_intervals(
    a: list[tuple[int, int]], b: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Находит пересечение двух списков интервалов."""
    # начальные индексы
    i, j = 0, 0
    result = []
    # цикл до тех пор, пока есть интервалы
    while i < len(a) and j < len(b):
        # получаем самый поздний старт интервалов
        start = max(a[i][0], b[j][0])
        # получаем самый ранний конец интервалов
        end = min(a[i][1], b[j][1])
        # если есть пересечение - добавляем в результат
        if start < end:
            result.append((start, end))
        # сдвигаем интервалы
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result


def appearance(intervals: dict[str, list[int]]) -> int:

    lesson_sessions = merge_intervals(intervals_to_sessions(intervals["lesson"]))
    pupil_sessions = merge_intervals(intervals_to_sessions(intervals["pupil"]))
    tutor_sessions = merge_intervals(intervals_to_sessions(intervals["tutor"]))

    lp_intersection = intersect_intervals(lesson_sessions, pupil_sessions)
    lpt_intersection = intersect_intervals(lp_intersection, tutor_sessions)

    return sum(end - start for start, end in lpt_intersection)

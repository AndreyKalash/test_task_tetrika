import unittest
from solution import (
    intervals_to_sessions,
    merge_intervals,
    intersect_intervals,
    appearance,
)


class TestIntervalsFunctions(unittest.TestCase):

    def test_intervals_to_sessions(self):
        intervals = [1, 2, 3, 4, 5, 6]
        expected = [(1, 2), (3, 4), (5, 6)]
        result = intervals_to_sessions(intervals)
        self.assertEqual(result, expected)

    def test_merge_intervals(self):
        intervals = [(1, 3), (2, 4), (5, 7), (6, 8)]
        expected = [(1, 4), (5, 8)]
        result = merge_intervals(intervals)
        self.assertEqual(result, expected)

    def test_intersect_intervals(self):
        a = [(1, 5), (10, 15), (20, 25)]
        b = [(3, 7), (14, 18), (22, 30)]
        expected = [(3, 5), (14, 15), (22, 25)]
        result = intersect_intervals(a, b)
        self.assertEqual(result, expected)


class TestAppearanceFunction(unittest.TestCase):

    def test_appearance(self):
        tests = [
            {
                "intervals": {
                    "lesson": [1594663200, 1594666800],
                    "pupil": [
                        1594663340,
                        1594663389,
                        1594663390,
                        1594663395,
                        1594663396,
                        1594666472,
                    ],
                    "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
                },
                "answer": 3117,
            },
            {
                "intervals": {
                    "lesson": [1594702800, 1594706400],
                    "pupil": [
                        1594702789,
                        1594704500,
                        1594702807,
                        1594704542,
                        1594704512,
                        1594704513,
                        1594704564,
                        1594705150,
                        1594704581,
                        1594704582,
                        1594704734,
                        1594705009,
                        1594705095,
                        1594705096,
                        1594705106,
                        1594706480,
                        1594705158,
                        1594705773,
                        1594705849,
                        1594706480,
                        1594706500,
                        1594706875,
                        1594706502,
                        1594706503,
                        1594706524,
                        1594706524,
                        1594706579,
                        1594706641,
                    ],
                    "tutor": [
                        1594700035,
                        1594700364,
                        1594702749,
                        1594705148,
                        1594705149,
                        1594706463,
                    ],
                },
                "answer": 3577,
            },
            {
                "intervals": {
                    "lesson": [1594692000, 1594695600],
                    "pupil": [1594692033, 1594696347],
                    "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
                },
                "answer": 3565,
            },
        ]

        for i, test in enumerate(tests):
            with self.subTest(f"Test case {i}"):
                result = appearance(test["intervals"])
                self.assertEqual(result, test["answer"], f"Failed on test case {i}")


if __name__ == "__main__":
    unittest.main()

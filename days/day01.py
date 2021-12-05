from helpers import *

test_data = Data("""
199
200
208
210
200
207
240
269
260
263
""")

test_case(1, test_data, 7)
test_case(2, test_data, 5)


def part1(d: Data, ans: Answers) -> None:
    ans.part1 = sum(
        i < j for (i, j) in zip(
            list(d.extract_ints),
            list(d.extract_ints[1:])
        )
    )


def part2(d: Data, ans: Answers) -> None:
    l = d.extract_ints

    def generate():
        for i in zip(l, l[1:], l[2:]):
            yield sum(i)

    sums = list(generate())
    ans.part2 = sum(
        i < j for (i, j) in zip(sums, sums[1:])
    )


run([1, 2], day=1, year=2021, submit=False)

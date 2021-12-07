from helpers import *

test_data = Input("""
3,4,3,1,2
""")

test_case(1, test_data, 5934)
test_case(2, test_data, 26984457539)


def part1_and_2(d: Input, ans: Answers) -> None:
    initial = d.extract_ints
    current = Counter(initial)

    for day in interval(1, 256):
        new = Counter()
        for k, v in current.items():
            if k == 0:
                new[6] += v
                new[8] += v
            else:
                new[k - 1] += v

        current = new

        if day == 80:
            ans.part1 = sum(current.values())

    ans.part2 = sum(current.values())


run([1, 2], day=6, year=2021)

from helpers import *

test_data = Data("""
3,4,3,1,2
""")

test_case(1, test_data, 5934)
test_case(2, test_data, 26984457539)


def part1_and_2(d: Data, ans: Answers) -> None:
    initial = d.extract_ints
    current = Counter(initial)

    for _ in range(256):
        new = Counter()
        for k, v in current.items():
            if k == 0:
                new[6] += v
                new[8] += v
            else:
                new[k - 1] += v
        current = new
        if _ == 79:
            ans.part1 = sum(current.values())

    ans.part2 = sum(current.values())


run([1, 2], day=6, year=2021, submit=True)

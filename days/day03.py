from helpers import *

test_data = Input("""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""")

test_case(1, test_data, 198)
test_case(2, test_data, 230)


def part1(d: Input, ans: Answers) -> None:
    cts = Counter()
    for i, in d.parsed_lines('<>'):
        for pos, bit in enumerate(i):
            cts[pos] += 1 if bit == '1' else -1
        l = len(i)

    gamma_rate = 0
    for i in range(l):
        gamma_rate <<= 1
        gamma_rate |= int(cts[i] >= 1)

    mask = 2 ** l - 1
    epsilon_rate = mask - gamma_rate
    ans.part1 = gamma_rate * epsilon_rate


def filter_values(numbers, position, most_common):
    one_bias = 0
    for i in numbers:
        one_bias += 1 if i & position else -1

    one_most_common = one_bias >= 0
    chosen = one_most_common

    if not most_common:
        chosen = not chosen

    filtered = [i for i in numbers if bool(i & position) == chosen]
    if len(filtered) == 1:
        return filtered[0]
    else:
        return filter_values(filtered, position >> 1, most_common)


def part2(d: Input, ans: Answers) -> None:
    cts = Counter()
    numbers = []
    for i, in d.parsed_lines('<>'):
        numbers.append(int(i, 2))
        l = len(i)

    answer1 = filter_values(numbers, position=1 << (l - 1), most_common=True)
    answer2 = filter_values(numbers, position=1 << (l - 1), most_common=False)
    ans.part2 = answer1 * answer2


run([1, 2], day=3, year=2021, submit=False)

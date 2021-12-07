import math

from helpers import *

test_data = Input("""
16,1,2,0,4,2,7,1,2,14
""")

test_case(1, test_data, 37)
test_case(2, test_data, 168)


def part1_and_2(d: Input, ans: Answers) -> None:
    positions = d.extract_ints

    ans.part1 = math.inf
    ans.part2 = math.inf

    for i in range(min(positions), max(positions)):
        fuel_part1 = fuel_part2 = 0

        for j in positions:
            distance = abs(j - i)
            fuel_part1 += distance

            # Thanks, Gauss
            fuel_part2 += (distance * (distance + 1) // 2)

        ans.part1 = min(ans.part1, fuel_part1)
        ans.part2 = min(ans.part2, fuel_part2)


run([1, 2], day=7, year=2021)

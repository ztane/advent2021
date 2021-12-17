from helpers import *

test_data = Input("""
target area: x=20..30, y=-10..-5
""")

test_case(1, test_data, 45)
test_case(2, test_data, 112)


def part1_and_2(d: Input, ans: Answers) -> None:
    x1, x2, y1, y2 = d.parsed('target area: x=<int>..<int>, y=<int>..<int>')

    bottom = min(y1, y2)
    initial_speed = -bottom - 1

    totals = 0
    for j in interval(1, initial_speed):
        totals += j

    ans.part1 = totals

    unique_hitting_vs = 0
    for vx, vy in product(interval(1, x2 + 1), interval(bottom - 1, -bottom + 1)):
        x = y = 0
        while y >= bottom:
            x += vx
            y += vy
            if vx > 0:
                vx -= 1
            vy -= 1

            if x1 <= x <= x2 and y1 <= y <= y2:
                unique_hitting_vs += 1
                break

    ans.part2 = unique_hitting_vs


run([1, 2], day=17, year=2021, submit=True)

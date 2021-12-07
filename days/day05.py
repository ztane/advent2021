from helpers import *

test_data = Input("""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""")

test_case(1, test_data, 5)
test_case(2, test_data, 12)


def part1(d: Input, ans: Answers) -> None:
    the_map = SparseMap(default=0)

    for x1, y1, x2, y2 in d.parsed_lines('<int>,<int> -> <int>,<int>'):
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                the_map[x1, y] += 1

        if y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                the_map[x, y1] += 1

    ans.part1 = sum(i > 1 for i in the_map.values())


def part2(d: Input, ans: Answers) -> None:
    the_map = SparseMap(default=0)

    for x1, y1, x2, y2 in d.parsed_lines('<int>,<int> -> <int>,<int>'):
        dx = int(abs(x2 - x1))
        dy = int(abs(y2 - y1))
        length = max(dx, dy)

        vx = (x2 - x1) // length
        vy = (y2 - y1) // length
        for i in range(length + 1):
            the_map[x1 + vx * i, y1 + vy * i] += 1

    ans.part2 = sum(i > 1 for i in the_map.values())


run([1, 2], day=5, year=2021, submit=False)

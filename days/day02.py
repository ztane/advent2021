from helpers import *

test_data = Input("""
forward 5
down 5
forward 8
up 3
down 8
forward 2
""")

test_case(1, test_data, 150)
test_case(2, test_data, 900)

directions = {
    'forward': 1,
    'down': 1j,
    'up': -1j
}

def part1(d: Input, ans: Answers) -> None:
    coords = 0

    for direction, length in d.parsed_lines('<> <int>'):
        coords += length * directions[direction]

    ans.part1 = int(coords.imag * coords.real)


def part2(d: Input, ans: Answers) -> None:
    coords = 0
    aim = 0

    for direction, length in d.parsed_lines('<> <int>'):
        coords += length * directions[direction].real
        coords += length * directions[direction].real * aim * 1j
        aim += length * directions[direction].imag

    ans.part2 = int(coords.imag * coords.real)


run([1, 2], day=2, year=2021, submit=False)

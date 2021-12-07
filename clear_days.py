
for i in range(2, 25):
    with open(f'days/day{i:02d}.py', 'w') as f:
        f.write(f"""\
from helpers import *

test_data = Input(\"\"\"
\"\"\")

test_case(1, test_data, ...)
test_case(2, test_data, ...)


def part1(d: Input, ans: Answers) -> None:
    ...


def part2(d: Input, ans: Answers) -> None:
    ...


run([1], day={i}, year=2021, submit=True)
""")

import itertools

from helpers import *


test_data = Input(r"""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce
""".replace('|\n', '| '))

test_case(1, test_data, 26)
test_case(2, test_data, 61229)

all_digits = 'abcdefg'
digit_map = {
    'ab': '1',
    'abcdef': '9',
    'abcdefg': '8',
    'abcdeg': '0',
    'abcdf': '3',
    'abd': '7',
    'abef': '4',
    'acdfg': '2',
    'bcdef': '5',
    'bcdefg': '6'
}


def part1(d: Input, ans: Answers) -> None:
    ct = 0
    for i in d.lines:
        print(i)
        k, l = i.split('|')
        l = l.strip()
        for j in l.split():
            if len(j) in {2, 3, 4, 7}:
                ct += 1
    ans.part1 = ct


def solve_digit_wiring(digits: Iterable[str]):
    """
    Find the wiring from the outputs to the 7-segment display input
    signals by finding such a permutation that all map to the normalized digits
    """
    for i in itertools.permutations('abcdefg'):
        translator = make_translator(''.join(i), all_digits)
        permuted = {charsort(translator(d)) for d in digits}
        if permuted.issubset(digit_map.keys()):
            return {d: digit_map[charsort(translator(d))] for d in digits}

    raise ValueError("no mapping")


def part2(d: Input, ans: Answers) -> None:
    ans.part2 = 0
    for i in d.lines:
        extra, output = [
            [charsort(d) for d in part.split()]
            for part in i.split('|')
        ]

        solved = solve_digit_wiring({*output, *extra})

        result_digits = ''.join(
            solved[d] for d in output
        )

        ans.part2 += int(result_digits)


run([1, 2], day=8, year=2021, submit=True)

from helpers import *

test_data = Input("""
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""")

test_case(1, test_data, 26397)
test_case(2, test_data, 288957)

part1_score_table = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

part2_score_table = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

opening_to_closing = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}


def part1_and_2(inp: Input, answers: Answers) -> None:
    answers.part1 = 0
    part2_scores = []

    for line in inp.lines:
        expected_closing = better_list()

        for char in line:
            if char in opening_to_closing:
                expected_closing.append(opening_to_closing[char])

            elif char != expected_closing.pop(-1, None):
                answers.part1 += part1_score_table[char]
                break

        else:
            part2_scores.append(reduce(
                lambda prev_score, c: 5 * prev_score + part2_score_table[c],
                reversed(expected_closing),
                0
            ))

    answers.part2 = median(filter(bool, part2_scores))


run([1, 2], day=10, year=2021)

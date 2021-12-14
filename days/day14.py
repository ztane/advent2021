from helpers import *

test_data = Input("""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""")

test_case(1, test_data, 1588)
test_case(2, test_data, 2188189693529)


def part1_and_2(d: Input, ans: Answers) -> None:
    template, instructions = d.paragraphs()
    instruction_map = {
        tuple(pair): new
        for pair, new in instructions.parsed_lines('<> -> <>')
    }

    @lru_cache(maxsize=None)
    def get_counts(pair: Tuple[str, str], depth: int) -> Counter[str]:
        if pair not in instruction_map or depth <= 0:
            return Counter([pair[0]])

        middle = instruction_map[pair]
        return (
                get_counts((pair[0], middle), depth - 1)
                + get_counts((middle, pair[1]), depth - 1)
        )

    counts = Counter()
    for pair in pairwise(template):
        counts += get_counts(pair, 10)

    counts[template[-1]] += 1
    ans.part1 = max(counts.values()) - min(counts.values())

    counts = Counter()
    for pair in pairwise(template):
        counts += get_counts(pair, 40)

    counts[template[-1]] += 1
    ans.part2 = max(counts.values()) - min(counts.values())
    print('Cache statistics:', get_counts.cache_info())


run([1, 2], day=14, year=2021, submit=True)

from helpers import *

test_data = Input("""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""")

test_data2 = Input("""
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""")

test_data3 = Input("""
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""")

test_case(1, test_data, 10)
test_case(1, test_data2, 19)
test_case(1, test_data3, 226)
test_case(2, test_data, 36)


# test_case(2, test_data2, 103)


def part1_and_2(d: Input, ans: Answers) -> None:
    conns = defaultdict(list[str])
    for a, b in d.parsed_lines('<>-<>'):
        conns[a].append(b)
        conns[b].append(a)

    def count_routes(
            node: list[str],
            visited_lwr: dict[str],
            max_visit_to_single: int
    ):
        c = 0
        for i in node:
            if i == 'start':
                continue

            if i in visited_lwr:
                if any(i >= max_visit_to_single for i in visited_lwr.values()):
                    continue

            if i == 'end':
                c += 1
                continue

            new_visited_lwr = visited_lwr
            if i.islower():
                new_visited_lwr = {**visited_lwr, i: visited_lwr.get(i, 0) + 1}

            c += count_routes(conns[i], new_visited_lwr, max_visit_to_single)

        return c

    ans.part1 = count_routes(conns['start'], {}, 1)
    ans.part2 = count_routes(conns['start'], {}, 2)


run([1, 2], day=12, year=2021)

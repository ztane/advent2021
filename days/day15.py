from helpers import *

test_data = Input("""
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""")

test_case(1, test_data, 40)
test_case(2, test_data, 315)


def part1_and_2(input_: Input, ans: Answers) -> None:
    init_map = SparseMap(input_.lines, converter=int)
    init_map.reset_size()
    map = SparseMap()
    w = init_map.columns
    h = init_map.rows

    def wrap(v):
        while v > 9:
            v -= 9
        return v

    for xr in range(5):
        for yr in range(5):
            for x in range(w):
                for y in range(h):
                    map[xr * w + x, yr * h + y] = wrap(init_map[x, y] + xr + yr)

    map.reset_size()
    minx = miny = 0
    maxx = map.columns - 1
    maxy = map.rows - 1

    def neighbours_func_part1(p: Tuple[int, int]) -> Tuple[Number, Tuple[int, int]]:
        for x, y in neighbourhood_4(p[0], p[1], init_map.is_inside):
            yield map[x, y], (x, y)

    def neighbours_func(p: Tuple[int, int]) -> Tuple[Number, Tuple[int, int]]:
        for x, y in neighbourhood_4(p[0], p[1], map.is_inside):
            yield map[x, y], (x, y)

    distance, _ = a_star_solve(
        (0, 0),
        target=(init_map.columns - 1, init_map.rows - 1),
        neighbours=neighbours_func_part1,
        heuristic=lambda p1, p2: abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
    )

    ans.part1 = distance

    distance_part2, _ = a_star_solve(
        (0, 0),
        target=(map.columns - 1, map.rows - 1),
        neighbours=neighbours_func,
        heuristic=lambda p1, p2: abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
    )

    ans.part2 = distance_part2


run([1, 2], day=15, year=2021, submit=True)

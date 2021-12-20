from scipy import ndimage

from helpers import *

test_data = Input("""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""")


test_case(1, test_data, 35)
test_case(2, test_data, 3351)


def part1_and_2(d: Input, ans: Answers) -> None:
    algo, data = d.replace('.', '0 ').replace('#', '1 ').paragraphs()
    value_mask = np.array([2 ** i for i in range(8, -1, -1)])
    masks = algo.extract_ints
    the_map = data.numpy_array

    def binfunc(window):
        return masks[int((window * value_mask).sum())]

    for i in range(50):
        the_map = np.pad(
            the_map,
            1,
            mode='constant',
            constant_values=i & masks[0]
        )

        the_map = ndimage.generic_filter(
            the_map,
            binfunc,
            size=3,
            mode='constant',
            cval=i & masks[0]
        )

        if i == 1:
            ans.part1 = int(the_map.sum())

    ans.part2 = int(the_map.sum())


run([1, 2], day=20, year=2021, submit=True)

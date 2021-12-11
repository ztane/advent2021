from scipy.ndimage import label, generate_binary_structure, minimum_filter

from helpers import *

test_data = Input("""
2199943210
3987894921
9856789892
8767896789
9899965678
""")

test_case(1, test_data, 15)
test_case(2, test_data, 1134)


def part1_and_2(d: Input, ans: Answers) -> None:
    the_map = d.digit_array_to_ndarray()

    # generate 1-connected rank 2 structure... i.e. 4-neighbourhood
    neighbourhood = generate_binary_structure(rank=2, connectivity=1)

    # use a minimum filter to replace all elements with the minima
    # in the neighbourhood. If this matches the original point then
    # this is local minimum in the neighbourhood, and results in true.
    # Solid areas of 9 will also result in trues in the middle -
    # we need to remove them
    local_minima = (minimum_filter(
        the_map, footprint=neighbourhood, mode='constant', cval=9
    ) == the_map) & (the_map != 9)

    # just calculate
    ans.part1 = np.sum(the_map[local_minima] + 1)

    # label the connected areas of any pixels < 9. Conveniently
    # the default neighbourhood for label is the one we want.
    features, _ = label(the_map < 9)

    # count the pixels thus created. Note that np.nditer yields
    # scalar "arrays" and therefore must be itemized in order to be
    # used in counter. Ignore background (value 0)
    counter = Counter(e.item() for e in np.nditer(features) if e)

    # product of # pixels in 3 most common labels.
    ans.part2 = prod(i[1] for i in counter.most_common(3))


run([1, 2], day=9, year=2021)

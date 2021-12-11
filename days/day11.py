import numpy
import scipy.ndimage

from helpers import *

test_data = Input("""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""")

test_case(1, test_data, 1656)
test_case(2, test_data, 195)


def part1_and_2(d: Input, ans: Answers) -> None:
    image = d.digit_array_to_ndarray()
    total = 0
    n_pixels = image.size

    for iteration in count(1):
        image += 1

        flashes_in_iteration = numpy.zeros_like(image, dtype='bool')
        while True:
            new_flashes = (image > 9) ^ flashes_in_iteration
            for y, x in np.transpose(np.where(new_flashes)):
                clamping_slicer(image)[y - 1:y + 2, x - 1:x + 2] += 1

            if np.sum(new_flashes) == 0:
                n_flashes = np.sum(flashes_in_iteration)

                if n_flashes == n_pixels:
                    ans.part2 = iteration
                    return

                total += n_flashes
                image[flashes_in_iteration] = 0
                break

            flashes_in_iteration |= new_flashes

        if iteration == 100:
            ans.part1 = total


run([1, 2], day=11, year=2021, submit=True)

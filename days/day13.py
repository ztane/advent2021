from helpers import *

test_data = Input("""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""")

test_case(1, test_data, 17)
test_case(2, test_data, 0)


def part1_and_2(d: Input, ans: Answers) -> None:
    coords, folds = d.split('\n\n')
    the_map = SparseMap()
    for x, y in coords.parsed_lines('<int>,<int>'):
        the_map[x, y] = 1

    for fold1_dir, fold1_coord in folds.parsed_lines('fold along <>=<int>'):
        new_map = SparseMap()

        for x, y in the_map:
            if fold1_dir == 'y' and fold1_coord < y:
                y = fold1_coord - (y - fold1_coord)
            if fold1_dir == 'x' and fold1_coord < x:
                x = fold1_coord - (x - fold1_coord)
            new_map[x, y] = 1

        if ans.part1 is None:
            ans.part1 = sum(new_map.values())

        the_map = new_map

    the_map.reset_size()
    the_map.print(mapping=lambda x: {None: ' ', 1: '\u2588'}[x])

    # fruitless attempts at OCRing
    """
    img = Image.new('L', (the_map.columns + 20, the_map.rows + 20), color=255)
    for x, y in the_map:
        img.putpixel((x + 10, y + 10), 0)

    img = img.resize(
        (img.size[0] * 8, img.size[1] * 8),
        resample=PIL.Image.BILINEAR
    )

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    code = pytesseract.image_to_string(img, config='--psm 7 --oem 1 -c tesseract_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    print('recognized', code)
    """

    ans.part2 = 0


run([1, 2], day=13, year=2021)

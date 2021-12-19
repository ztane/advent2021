import dataclasses

from scipy.spatial.distance import cdist

from helpers import *

test_data = Input("""
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""")

test_case(1, test_data, 79)
test_case(2, test_data, 3621)


def unit_vector_rotations():
    i = np.array([1, 0, 0])
    j = np.array([0, 1, 0])
    k = np.array([0, 0, 1])

    rotations = []
    for i in permutations([i, j, k], 2):
        for signs in product([-1, 1], repeat=2):
            vec1 = i[0] * signs[0]
            vec2 = i[1] * signs[1]
            vec3 = np.cross(vec1, vec2)

            rotations.append(np.array([vec1, vec2, vec3]))

    return rotations


def part1_and_2(d: Input, ans: Answers) -> None:
    scanners: List[np.ndarray] = []
    for scanner in d.paragraphs():
        _, coords = scanner.split('\n', 1)
        scanners.append(coords.numpy_array)

    all_beacons = scanners.pop(0)

    rotations = unit_vector_rotations()

    mapped = set()
    scanner_coordinates = [(0, 0, 0)]

    while len(mapped) < len(scanners):
        for i in range(len(scanners)):
            if i in mapped:
                continue

            this_scanner = scanners[i]
            for j in rotations:
                reoriented = j.dot(this_scanner.T).T
                counts = Counter()
                for row in reoriented:
                    totals = all_beacons - row
                    counts.update(map(tuple, totals))

                if counts.most_common(1)[0][1] >= 12:
                    translation = counts.most_common(1)[0][0]
                    scanner_coordinates.append(translation)
                    reoriented += np.array(translation)
                    all_beacons = np.unique(np.concatenate((all_beacons, reoriented)), axis=0)
                    mapped.add(i)
                    break

    ans.part1 = all_beacons.shape[0]

    max_manhattan = 0

    def manhattan_distance(a, b):
        return np.abs(np.array(a) - np.array(b)).sum()

    for a, b in combinations(scanner_coordinates, 2):
        max_manhattan = max(manhattan_distance(a, b), max_manhattan)

    ans.part2 = max_manhattan


run([1, 2], day=19, year=2021, submit=True)

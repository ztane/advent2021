import ast
import dataclasses

from helpers import *

test_data = Input("""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""")


test_case(1, test_data, 4140)
test_case(2, test_data, 3993)


@dataclasses.dataclass
class Node:
    left: Node | int = None
    right: Node | int = None
    parent: Node | None = dataclasses.field(default=None, repr=False)

    def __post_init__(self):
        if isinstance(self.left, Node):
            self.left.parent = self

        if isinstance(self.right, Node):
            self.right.parent = self

    def get(self, side: str) -> Node | int:
        return getattr(self, side)

    def set(self, side: str, value: int):
        return setattr(self, side, value)

    def __repr__(self):
        return f'[{self.left!r},{self.right!r}]'


def to_sf_number(l) -> Node | int:
    if isinstance(l, int):
        return l

    return Node(to_sf_number(l[0]), to_sf_number(l[1]))


def reduce_sf_number(number: Node):
    labelled = []

    def label(node: Node = number, depth=1):
        if depth == 1:
            labelled.clear()

        if isinstance(node.left, int):
            labelled.append((node, 'left', node.left, depth))
        else:
            label(node.left, depth + 1)

        if isinstance(node.right, int):
            labelled.append((node, 'right', node.right, depth))
        else:
            label(node.right, depth + 1)

    def explode() -> bool:
        for i, e in enumerate(labelled):
            if e[3] >= 5:
                # found node to explode
                node: Node = e[0]
                if i > 0:
                    left_side, side, value, _ = labelled[i - 1]
                    new_value = value + node.left
                    left_side.set(side, new_value)

                if i < len(labelled) - 2:
                    right_side, side, value, _ = labelled[i + 2]
                    new_value = value + node.right
                    right_side.set(side, new_value)

                if node.parent.left is node:
                    node.parent.left = 0

                if node.parent.right is node:
                    node.parent.right = 0

                return True

        return False

    def split() -> bool:
        for node, side, value, depth in labelled:
            if value >= 10:
                new_node = Node(value // 2, (value + 1) // 2)
                new_node.parent = node
                node.set(side, new_node)
                return True

        return False

    while True:
        label(number)

        if explode():
            continue

        if split():
            continue

        break

    return number


def add_sf_numbers(a: Node | int, b: Node | int) -> Node:
    result = Node(a, b)
    result = reduce_sf_number(result)
    return result


def sf_number_magnitude(node: Node | int):
    if isinstance(node, int):
        return node

    return 3 * sf_number_magnitude(node.left) + 2 * sf_number_magnitude(node.right)


def part1(d: Input, ans: Answers) -> None:
    final_sum = reduce(
        add_sf_numbers,
        map(to_sf_number, map(ast.literal_eval, d.splitlines()))
    )
    ans.part1 = sf_number_magnitude(final_sum)


def part2(d: Input, ans: Answers) -> None:
    max_num = 0
    for i, j in permutations(map(ast.literal_eval, d.splitlines()), 2):
        if i is j:
            continue

        max_num = max(max_num, sf_number_magnitude(add_sf_numbers(
            to_sf_number(i), to_sf_number(j)
        )))

    ans.part2 = max_num


assert sf_number_magnitude(to_sf_number([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])) == 3488

run([1, 2], day=18, year=2021, submit=True)

import dataclasses

# noinspection PyUnresolvedReferences
import inspect
import operator as op
import re
import typing
from collections import *
# noinspection PyUnresolvedReferences
from dataclasses import dataclass
from functools import *
# noinspection PyUnresolvedReferences
from hashlib import md5
# noinspection PyUnresolvedReferences
from heapq import *
# noinspection PyUnresolvedReferences
from itertools import *

builtin_pow = pow
from math import *

from numbers import *
# noinspection PyUnresolvedReferences
from textwrap import dedent
# noinspection PyUnresolvedReferences
from typing import *
from typing import Union, Dict

from aocd import get_data, submit as _aocd_submit
import numpy as np


class reify(object):
    """
    Rip of `reify` from Pyramid framework.

    Use as a class method decorator.  It operates almost exactly like the
    Python ``@property`` decorator, but it puts the result of the method it
    decorates into the instance dict after the first call, effectively
    replacing the function it decorates with an instance variable.  It is, in
    Python parlance, a non-data descriptor.
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        update_wrapper(self, wrapped)

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


class Input(str):
    def __new__(cls, data: str):
        data = data.strip('\r\n')
        rv = super().__new__(cls, data.strip('\r\n'))
        rv.data = data
        return rv

    @reify
    def lines(self) -> typing.Tuple['Input', ...]:
        return tuple(
            filter(bool,
                   map(Input,
                       map(str.rstrip, self.data.splitlines()))
                   ))

    def stripsplit(self, separator: str = None, maxsplit=-1) -> typing.List[
        'Input']:
        """
        Split with the desired separator and also strip whitespace from parts
        """
        return [
            Input(i.strip())
            for i in self.data.split(separator, maxsplit=maxsplit)
        ]

    def split(self, separator: str = None, maxsplit=-1) -> typing.List['Input']:
        return [Input(i) for i in self.data.split(separator, maxsplit=maxsplit)]

    @reify
    def as_int(self) -> int:
        return int(self.data)

    @reify
    def as_ints(self) -> typing.Tuple[int, ...]:
        return tuple(map(int, re.findall(r'-?\d+', self.data)))

    @reify
    def as_unsigned(self) -> typing.Tuple[int, ...]:
        return tuple(map(int, re.findall(r'\d+', self.data)))

    @reify
    def extract_unsigned(self) -> typing.Tuple[int, ...]:
        return tuple(map(int, re.findall(r'\d+', self.data)))

    @reify
    def extract_ints(self) -> typing.Tuple[int, ...]:
        return tuple(map(int, re.findall(r'-?\d+', self.data)))

    @reify
    def sentences(self) -> typing.List[typing.List[str]]:
        """
        Assume the data is

        :return:
        """
        return [
            i.split() for i in self.lines
        ]

    @reify
    def integer_matrix(self) -> typing.List[typing.List[int]]:
        """
        Assume the data is a 2-dimensional space-separated integer matrix

        :return: that matrix
        """
        return [[int(i) for i in line.split()] for line in self.lines]

    @reify
    def numpy_array(self) -> np.ndarray:
        return np.array(self.integer_matrix)

    def parsed_lines(self, fmt: str, verbatim_ws: bool = False) \
            -> typing.Iterator[typing.Tuple]:
        """
        Return the data parsed with a single parser
        :param fmt: the format
        :param verbatim_ws: whether verbatim boolean is used
        :return: iterator of parsed tuples
        """

        return Parser(fmt, verbatim_ws=verbatim_ws).for_lines(self.lines)

    def print_excerpt(self) -> None:
        """
        Print an excerpt of the data. Maximum of 10 lines followed by
        how many lines were omitted
        :return: None
        """
        lines = list(enumerate(self.lines, 1))
        print("-" * 78)

        def printline(i):
            lineno, line = i
            print(f"{lineno:-5d}: {line}")

        if len(lines) > 12:
            for i in lines[:5]:
                printline(i)

            print(f'[ {len(lines)} lines in total; {len(lines) - 10} '
                  f'lines omitted... ]')

            for i in lines[-5:]:
                printline(i)

        else:
            for l in lines:
                printline(l)

        print("-" * 78)

    @reify
    def without_spaces(self) -> str:
        return ''.join(i for i in self if not i.isspace())

    def parsed(self, format) -> 'Parser':
        return Parser(format)(self)


class IntersectionSet(set):
    """
    A set whose intersection_update counts the intersection of
    *all* times the intersection is called. I.e. an uninitialized
    set is considered to contain all possible elements.
    """

    def __init__(self, iterable=None):
        self._is_set = False
        if iterable:
            super().__init__(iterable)
            self._is_set = True
        else:
            super().__init__()

    def update(self, iterable) -> None:
        self._is_set = True
        super().update(iterable)

    def intersection_update(self, *s: Iterable[Any]) -> None:
        if not self._is_set:
            super().update(*s)
            self._is_set = True

        else:
            super().intersection_update(*s)


def get_aoc_data(day: int, year=None) -> Input:
    """
    Get the wrapped AOC data for a given day

    :param day: the day
    :return: the data
    """

    rv = Input(get_data(day=day, year=year, block=True))
    rv.print_excerpt()
    return rv


def clamp(value: int, min_: int, max_: int) -> int:
    """
    Clamp the value so that it is at least min_ and at most max_

    :param value: the value
    :param min_: the minimum
    :param max_: the maximum
    :return: min_, max_, or value, iff min_ <= value <= max_
    """

    if value < min_:
        return min_
    if value > max_:
        return max_
    return value


def ngrams(n: int, value: Sequence) -> typing.Iterator[Sequence]:
    """
    Given a *sequence*, return its n-grams

    :param value: the value, can be list, tuple, or str
    :return: *generator* of the ngrams
    """

    for i in range(len(value) - n + 1):
        yield value[i:i + n]


def items(thing, *indexes):
    """
    Return the given indexes of the item as a tuple

    :param thing: the thing to index
    :param indexes: indexes
    :return: tuple of the items
    """
    return op.itemgetter(*indexes)(thing)


def to_ints(container: typing.Collection[typing.Any]) -> typing.Collection[
    float]:
    """
    Return the given items as ints, in the same container type

    :param container: the items
    :return: the items as ints
    """

    t = type(container)
    return t(map(int, container))


def to_floats(container: typing.Collection[typing.Any]) -> typing.Collection[
    float]:
    """
    Return the given items as floats, in the same container type

    :param container: the items
    :return: the items as ints
    """

    t = type(container)
    return t(map(float, container))


def every_nths(iterable, n=2):
    """
    return n lists of every nth elements; first list contains item
    0, second list item 1 and so forth

    :param iterable: the iterable to iterate over. Will be converted
        to a list internally
    :return: list of lists
    """

    as_list = list(iterable)
    return [as_list[i::n] for i in range(n)]


def get_ints(s):
    """
    Return all decimal integers in the given string
    as a sequence

    :param s: a string
    :return: sequence of integers
    """
    return list(map(int, re.findall('\d+', s)))


def draw_display(display_data):
    """
    Draw pixel display (row, column matrix)

    :param display_data: the display data
    :return: None
    """
    row_length = len(display_data[0])
    print('-' * row_length)
    for row in display_data:
        for column in row:
            print([' ', '\033[42m \033[0m'][bool(column)], end='')
        print()
    print('-' * row_length)


_parser_conversions = {
    'int': (int, r'\s*[-+]?\d+\s*'),
    'str': (Input, r'.*?'),
    'chr': (Input, r'.'),
    'hex': (lambda x: int(x, 16), r'\s*[-+]?[0-9a-fA-F]+\s*'),
}


class Parser:
    """
    A parser class for parsing fields from a single
    formatted input string.
    """
    last_val = None

    def __init__(self, fmt, verbatim_ws=False):
        """
        Initialize the parser class, with given format

        :param fmt: the format string
        :param verbatim_ws: if false, spaces are replaced with
            \s+, if true, space characters must match exactly
        """
        regex = ''
        pos = 0

        self.matched = False
        self.items = ()
        self.conversions = []

        while pos < len(fmt):
            c = fmt[pos]
            pos += 1
            if c == '<':
                if fmt[pos] == '<':
                    regex += r'\<'
                    pos += 1
                else:
                    end = fmt.index('>', pos)
                    pattern = fmt[pos:end]
                    suppress = False
                    if pattern.startswith('*'):
                        # suppress listing
                        pattern = pattern[1:]
                        suppress = True

                    pattern = pattern or 'str'

                    conversion, _, pattern = pattern.partition(':')
                    convfunc, default_re = _parser_conversions[conversion]
                    if not pattern:
                        pattern = default_re
                    regex += '({})'.format(pattern)
                    self.conversions.append((convfunc, suppress))
                    pos = end + 1

            else:
                if c == ' ' and not verbatim_ws:
                    regex += r'\s+'
                else:
                    regex += re.escape(c)

        self.regex = re.compile(regex)

    def __call__(self, string: str) -> 'Parser':
        """
        Match the given string against the pattern, and set results
        :param string: the string
        :return: self for chaining and truth-value checking
        """
        m = self.regex.fullmatch(string)
        self.matched = bool(m)
        self.last_val = string
        if m:
            self.items = tuple(
                self._convert(m, convfunc, group)
                for (group, (convfunc, suppress)) in
                enumerate(self.conversions, 1)
                if not suppress
            )
        else:
            self.items = ()

        return self

    def for_lines(self, lines):
        for line in lines:
            yield tuple(self(line))

    def _convert(self, match, convfunc, group):
        val = match.group(group)
        if val is not None:
            return convfunc(val)
        return None

    def __bool__(self) -> bool:
        return self.matched

    def __iter__(self) -> Iterator[Any]:
        if not self.matched:
            raise ValueError(
                'The pattern didn\'t match {}'.format(self.last_val))

        return iter(self.items)

    def __len__(self) -> int:
        if not self.matched:
            raise ValueError('The pattern didn\'t match')

        return len(self.items)

    def __getitem__(self, i):
        if not self.matched:
            raise ValueError('The pattern didn\'t match')

        return self.items[i]


@total_ordering
class Node:
    __slots__ = ('heuristic', 'distance', 'state')

    def __init__(self, heuristic, distance, state):
        self.heuristic = heuristic
        self.distance = distance
        self.state = state

    def __eq__(self, other):
        return ((self.heuristic, self.distance) ==
                (other.heuristic, other.distance))

    def __lt__(self, other):
        return self.heuristic + self.distance < other.heuristic + other.distance

    def __iter__(self):
        return iter((self.heuristic, self.distance, self.state))


def neighbourhood_4(x, y, valid=lambda x, y: True):
    neighbours = []
    for nx, ny in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
        if valid(nx, ny):
            neighbours.append((nx, ny))

    return neighbours


def neighbourhood_8(x, y, valid=lambda x, y: True):
    neighbours = []
    for nx, ny in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1),
                   (x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1),
                   (x - 1, y + 1)):
        if valid(nx, ny):
            neighbours.append((nx, ny))

    return neighbours


def neighbourhood_8_counts(x: int, y: int,
                           valuefunc: Callable[[int, int], Any]):
    counts = Counter()
    for nx, ny in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1),
                   (x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1),
                   (x - 1, y + 1)):
        counts[valuefunc(nx, ny)] += 1

    return counts


def a_star_solve(
        origin: Any,
        *,
        target: Optional[Any] = None,
        max_distance: Optional[Number] = None,
        neighbours: Callable[[Any], Tuple[Number, Any]],
        heuristic: Optional[Callable[[Any, Any], Number]] = None,
        is_target: Optional[Callable[[Any], bool]] = None,
        find_all: bool = False,
        hashable: Callable[[Any], Hashable] = lambda n: n
):
    if max_distance is None:
        max_distance = 2 ** 32

    if not heuristic:
        def heuristic(node, target):
            return 0

    queue = [Node(heuristic(origin, target), 0, origin)]
    visited = {hashable(origin)}

    if not is_target:
        def is_target(n):
            return n == target

    cnt = 0
    all_routes = []
    max_depth = 0

    min_h = heuristic(origin, target) + 1
    while queue:
        hx, distance, node = heappop(queue)
        if is_target(node):
            if not find_all:
                return distance, node
            else:
                all_routes.append((distance, node))
                continue

        visited.add(hashable(node))
        if distance > max_depth:
            max_depth = distance

        for d_dist, node in neighbours(node):
            if hashable(node) in visited:
                continue

            if distance + d_dist <= max_distance:
                h = heuristic(node, target)
                if h < min_h:
                    min_h = h
                heappush(queue, Node(h,
                                     distance + d_dist, node))

                cnt += 1

    if find_all:
        return all_routes
    return len(visited)


chained = chain.from_iterable


def lcm(a: int, b: int) -> int:
    """
    Returns the least common multiple of the 2 numbers
    :param a: number
    :param b: another
    :return: the lcm
    """
    return (a * b) // gcd(a, b)


def better_translator(table: Dict[str, str]) -> typing.Callable[[str], str]:
    """
    Returns a translator function that, given a string, will replace all
    the key strings to their corresponding values from the string, using
    maximal munch.

    :param table: the dictionary of strings to strings
    :return: a function, str->str
    """
    strings = '|'.join(re.escape(i) for i in table.keys())
    pattern = re.compile(strings)

    def replacement(m):
        return table[m.group(0)]

    def translate(s):
        return pattern.sub(replacement, s)

    return translate


def md5digest(s: Union[bytes, str]) -> str:
    """
    Return the md5 digest of the given argument as hex
    :param s: the string; either bytes or str
    :return: the hex digest, as a string
    """
    try:
        s = s.encode()
    except AttributeError:
        pass

    return md5(s).hexdigest()


def cinf_norm(val: complex) -> int:
    """
    Calculate the L_inf norm of the given complex number as an integer
    :param val: the number
    :return: the norm
    """
    return int(max(abs(val.real), abs(val.imag)))


def cmanhattan(val: complex) -> int:
    """
    Calculate the L_1 norm of the given complex number as an integer
    :param val: the number
    :return: the norm
    """
    return int(abs(val.real) + abs(val.imag))


def manhattan(*components: Real) -> Real:
    """
    Calculate the L_1 norm of the given components
    :param components: the real components
    :return: the norm
    """

    return sum(map(abs, components))


def spiral_walk() -> typing.Iterator[complex]:
    """
    Return the generator of the spiral walk, as in AOC 2017 puzzle 3.
    :return: the generator that yields successive coordinates as complex numbers
    in order.
    """
    coords = 0 + 0j
    direction = 1
    for max_d in count():
        # OEIS A022144
        looping = (2 * max_d + 1) ** 2 - (2 * max_d - 1) ** 2
        for i in range(looping):
            yield coords
            if cinf_norm(coords + direction) > max_d:
                direction *= 1j

            coords += direction

        coords += 1 - direction
        direction = 1


_CNEIGHBOURHOOD_8_WITH_SELF = list(x + y * 1j
                                   for (x, y)
                                   in product([-1, 0, 1], repeat=2))
_CNEIGHBOURHOOD_8 = [i for i in _CNEIGHBOURHOOD_8_WITH_SELF if i]


def cneighbours_8(point: complex,
                  *,
                  add_self: bool = False) -> typing.Iterator[complex]:
    """
    Return the 8-neighbourhood around the complex coordinates. If `add_self`
    is true, then return the point itself as well.

    :param add_self: boolean, add self into the value
    :return: a generator of neighbour coordinates
    """

    for delta in ((_CNEIGHBOURHOOD_8, _CNEIGHBOURHOOD_8_WITH_SELF)[add_self]):
        yield point + delta


class ring_list(list):
    """
    Fixed length list, with modular indexing
    """

    def __delitem__(self, key):
        raise NotImplemented

    def pop(self, *a, **kw):
        raise NotImplemented

    def __getitem__(self, item):
        if isinstance(item, slice):
            if item.stop is not None and item.stop < 0:
                raise ValueError('Slice indices must be non-negative')

            if item.start is not None and item.start < 0:
                raise ValueError('Slice indices must be non-negative')

            return [self[i] for i in range(*item.indices(2 ** 32))]

        return super().__getitem__(item % len(self))

    def __setitem__(self, item, value):
        if isinstance(item, slice):
            if item.stop and item.stop < 0:
                raise ValueError('Slice indices must be non-negative')

            if item.start and item.start < 0:
                raise ValueError('Slice indices must be non-negative')

            indices = range(*item.indices(2 ** 32))
            if len(indices) != len(value):
                raise ValueError('Slice length doesn\'t match')

            for i, e in zip(indices, value):
                self[i] = e

            return

        return super().__setitem__(item % len(self), value)

    def slice(self, start, end):
        return [self[i] for i in range(start, end)]

    def splice(self, start, assigned):
        for i, e in zip(range(start, start + len(assigned)), assigned):
            self[i] = e


class counting_set(dict):
    def __init__(self, iterator=None):
        super().__init__()
        if iterator is not None:
            for i in iterator:
                self.add(i)

    def add(self, item):
        if item not in self:
            self[item] = len(self) + 1


T = typing.TypeVar('T')


def find_unique(
        items: typing.Iterable[T],
        key: typing.Callable[[T], typing.Any] = lambda x: x
) -> typing.Optional[T]:
    """
    Find the one item that is unique keywise or none at all
    :param items: iterator of items
    :param key: anything
    :return: the one or none
    """

    keys_to_items = defaultdict(list)
    for i in items:
        keys_to_items[key(i)].append(i)

    candidates = []
    for i in keys_to_items.values():
        if len(i) == 1:
            candidates.append(i)

    if len(candidates) > 1:
        raise ValueError('More than one "unique"')

    if candidates:
        return candidates[0][0]

    return None


class IterableInt(int):
    def __getitem__(self, item: int) -> int:
        if item in self:
            return item

        raise IndexError

    def __contains__(self, value: int) -> bool:
        return 0 <= value < self

    def __iter__(self) -> Iterable[int]:
        return iter(range(self))


class SparseMap(dict):
    rows: IterableInt
    columns: IterableInt

    def __init__(self, the_map=(), *, default=None):
        super().__init__()
        if callable(default):
            self.generate = default
        else:
            self.generate = lambda x, y: default

        y = -1
        x = -1
        max_x = -1
        for y, row in enumerate(the_map):
            for x, cell in enumerate(row):
                self[x, y] = cell

            max_x = max(x, max_x)

        self.rows = IterableInt(y + 1)
        self.columns = IterableInt(max_x + 1)

    def add_row(self, row) -> None:
        new_y = self.rows
        for x, cell in enumerate(row):
            self[x, new_y] = cell
        self.rows += 1

    def is_inside(self, x, y) -> bool:
        return 0 <= x < self.columns and 0 <= y < self.rows

    def __missing__(self, key):
        x, y = key
        self[key] = self.generate(x, y)
        if x >= self.columns:
            self.columns = IterableInt(x + 1)
        if y >= self.rows:
            self.rows = IterableInt(y + 1)

        return self[key]

    def print(self) -> 'SparseMap':
        for y in IterableInt(self.rows):
            for x in IterableInt(self.columns):
                print(self[x, y], end='')
            print()

        return self


def SparseRepeatingMap(basic_pattern):
    def generate(x, y):
        return basic_pattern[y % the_map.rows][x % the_map.columns]

    the_map = SparseMap(the_map=basic_pattern, default=generate)
    return the_map


class SparseComplexMap(dict):
    def __init__(self, the_map=(), *, default=None):
        super().__init__()
        if callable(default):
            self.generate = default
        else:
            self.generate = lambda x, y: default

        y = -1
        x = -1
        max_x = -1
        for y, row in enumerate(the_map):
            for x, cell in enumerate(row):
                self[x + y * 1j] = cell

            max_x = max(x, max_x)

        self.rows = y + 1
        self.columns = max_x + 1

    def add_row(self, row):
        new_y = self.rows
        for x, cell in enumerate(row):
            self[x + new_y * 1j] = cell
        self.rows += 1

    def __missing__(self, key):
        x, y = int(key.real), int(key.imag)
        self[key] = self.generate(x, y)
        return self[key]

    @property
    def center(self):
        if not self.columns % 2 or not self.rows % 2:
            raise ValueError('The width and height both must be odd')
        return complex(self.columns // 2, self.rows // 2)


def SparseRepeatingComplexMap(basic_pattern):
    def generate(x, y):
        return basic_pattern[y % the_map.rows][x % the_map.columns]

    the_map = SparseComplexMap(the_map=basic_pattern, default=generate)
    return the_map


def is_scalar(i: Any) -> bool:
    return not (isinstance(i, Iterable) and not isinstance(i, (str, bytes)))


def scalar(i: Iterable, nested: bool = False):
    """
    Returns the *one* element in the iterable, or throws ValueError
    :param i: the iterable
    :param nested: unfold nested iterables
    :return: the scalar value
    """

    while not is_scalar(i):
        l = list(i)
        if len(l) != 1:
            raise ValueError('The given iterable must have exactly one element,'
                             ' was {}'.format(i))
        i = l[0]
        if not nested:
            return i

    return i


def coords(i: Union[complex, Iterable]) -> str:
    """
    Convert the given thing whatever it is to nice coordinate string.
    :param i: the thing
    :return:
    """

    if isinstance(i, complex):
        return f'{int(i.real)},{int(i.imag)}'

    else:
        x, y = i
        return f'{int(x)},{int(y)}'


def interval(
        a: int | None = None,
        b: int | None = None,
        c: int | None = None,
        /
) -> range:
    """
    It is like range, but... inclusive.
    """
    if b is None:
        return range(a + 1)
    if c is None:
        return range(a, b + 1)

    return range(a, b + 1, c)


class fancyseqiter:
    def __init__(self, s: Sequence, start: int = 0):
        self._s = s
        self._i = start - 1
        self._l = len(self._s) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self._i >= self._l:
            raise StopIteration

        self._i += 1
        return self._s[self._i]

    def copy(self, adjustment=0):
        return fancyseqiter(self._s, self._i + adjustment)


def intersection(items: Iterable[T]) -> Set[T]:
    items = list(items)
    if not items:
        return set()

    return set(items[0]).intersection(*items[1:])


def union(items: Iterable[T]) -> Set[T]:
    items = list(items)
    if not items:
        return set()

    return set(items[0]).union(*items[1:])


def set_len(items: Iterable[T]) -> int:
    return len(set(items))


_test_cases = defaultdict(dict)


def test_case(part, input, output):
    _test_cases[part][input] = output


@dataclasses.dataclass()
class Answers:
    part1: Optional[Union[str, int]]
    part2: Optional[Union[str, int]]

    def __init__(self, part1: Any = None, part2: Any = None):
        self.part1 = part1
        self.part2 = part2

    def for_part(self, part: int) -> Any:
        if part == 1:
            return self.part1

        if part == 2:
            return self.part2

        raise ValueError(f"Unknown part number {part}")

    def print_answers(self):
        for part in [1, 2]:
            if self.for_part(part) is not None:
                print(f"Part {part}:")
                print(self.for_part(part))

    def submit(self, parts, day, year):
        for part in parts:
            # wim uses 'a' and 'b' for parts

            part_letter = '-ab'[part]
            answer = self.for_part(part)
            if answer is None:
                raise ValueError(f'The answer for part {part} is None')

            _aocd_submit(answer, part=part_letter, day=day, year=year)


def _test(parts, func):
    success = True
    had_cases = False

    for part in parts:
        for input, output in _test_cases[part].items():
            had_cases = True
            answers = Answers()
            func(Input(input), answers)

            if (answer := answers.for_part(part)) is None:
                raise ValueError(f"No answer was given for test case {input!r} "
                                 f"for part {part}, was expecting {output!r}")

            if str(answer) != str(output):
                print(
                    f"WARNING output {answer!s} from part {part} does not match"
                    f" test case output {output!s}")
                success = False

    if not had_cases:
        return None

    return success


def run(parts: Union[Iterable[int], int] = (1, 2),
        *, day, year, submit=False) -> None:
    caller_globals = inspect.stack()[1][0].f_globals

    if is_scalar(parts):
        parts = [parts]

    data = get_aoc_data(day=day, year=year)

    def get_data():
        return Input(str(data))

    both_parts = caller_globals.get("part1_and_2")
    if both_parts:
        test_success = _test(parts, both_parts)

        if test_success:
            print(f"100 % of the test cases succeeded")
        elif test_success is None:
            print("No test cases!")
        else:
            print("Test failure")

        answers = Answers()
        both_parts(get_data(), answers)
        answers.print_answers()

        if submit:
            if test_success or submit == 'force':
                answers.submit(parts, day=day, year=year)
            else:
                print("Refusing to submit automatically")
    else:
        for part in parts:
            func = caller_globals[f'part{part}']
            test_success = _test([part], func)

            if test_success:
                print(f"100 % of the test cases succeeded for part {part}")
            elif test_success is None:
                print("No test cases!")
            else:
                print(f"Test failure for part {part}")

            answers = Answers()
            func(get_data(), answers)
            answers.print_answers()

            if submit:
                if test_success or submit == "force":
                    answers.submit([part], day=day, year=year)
                else:
                    print("Refusing to submit automatically")


_direction_parser_prefix = re.compile('([newsNEWS]+)\s*(-?\d+)')
_direction_parser_suffix = re.compile('(-?\d+)\s*([newsNEWS]+)')


class cdir:
    """
    Complex directions
    """

    N = NORTH = -1j
    E = EAST = 1
    S = SOUTH = 1j
    W = WEST = -1

    NW = N + W
    NE = N + E
    SW = S + W
    SE = S + E

    @staticmethod
    def rotate_left(vector: complex, times: int = 1):
        return vector * ((-1j) ** times)

    @staticmethod
    def rotate_left_degrees(vector: complex, degrees: int = 90):
        return cdir.rotate_left(vector, degrees // 90)

    @staticmethod
    def rotate_right(vector: complex, times=1):
        return vector * (1j ** times)

    @staticmethod
    def rotate_right_degrees(vector: complex, degrees: int = 90):
        return cdir.rotate_right(vector, degrees // 90)

    @classmethod
    def compass(cls, direction: str, length: int = 1):
        return getattr(cls, direction.upper()) * length

    @classmethod
    def rotate_degrees(cls, vector: complex, direction: str,
                       number: int = 90) -> complex:
        direction = direction.upper()[0]

        if direction == 'L':
            return cls.rotate_left_degrees(vector, number)

        if direction == 'R':
            return cls.rotate_right_degrees(vector, number)

        raise ValueError(f'Invalid direction {direction}')

    @classmethod
    def parse(cls, string: str, prefix: bool = True) -> complex:
        rv = 0
        if prefix:
            for d, n in _direction_parser_prefix.findall(string):
                print(d, n)
                rv += cls.compass(d, int(n))
        else:
            for n, d in _direction_parser_prefix.findall(string):
                rv += cls.compass(d, int(n))

        return rv


@dataclass
class CRTSolution:
    lowest: int
    cycle: int


def crt(mods: List[Tuple[int, int]]) -> CRTSolution:
    """
    Use the Chinese Remainder Theorem
    """

    inc = 1
    current = 0

    for modulus, remainder in mods:
        while current % modulus != remainder:
            current += inc

        inc = lcm(inc, modulus)

    return CRTSolution(lowest=current, cycle=inc)


class ToggleSet(set):
    def toggle(self, value) -> None:
        if value not in self:
            self.add(value)
        else:
            self.discard(value)

    def copy(self) -> 'ToggleSet':
        return ToggleSet(self)


def charsort(s: str) -> str:
    """
    Return the string with its characters sorted
    """
    return ''.join(sorted(s))


def make_translator(original: Iterable[str], target: Iterable[str]) \
        -> Callable[[str], str]:
    """
    Returns a function that will translate the characters in the original
    sequence to the corresponding characters in the destination sequence.
    Each argument must be iterable of *characters* of equal length (i.e.
    strings of same length, or lists of strings of length 1...)
    """

    table = str.maketrans(''.join(original), ''.join(target))

    def translator(s: str) -> str:
        return s.translate(table)

    return translator

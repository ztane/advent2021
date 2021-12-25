from helpers import *

test_data = Input("""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#  
  #########  
""")

move_costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}
test_case(1, test_data, 12521)
test_case(2, test_data, 44169)


@dataclasses.dataclass(frozen=True, slots=True)
class Amphipod:
    t: str
    x: int
    y: int
    in_hallway: bool


target_rooms = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}


@lru_cache(maxsize=None)
def min_energy_to_solve(a: Amphipod):
    cost = 0
    if a.y != 1:
        cost += a.y - 1

        # need to move away from room end too!
        if a.x == target_rooms[a.t]:
            cost += 2

    cost += abs(a.x - target_rooms[a.t])

    # move in to first place
    cost += 1

    return move_costs[a.t] * cost


coordinates = Tuple[int, int]


class StateGenerator:
    map_: SparseMap
    target_rooms_by_type: Dict[str, List[coordinates]]
    state_encoder: List[coordinates]
    targettable_rooms: Set[str]

    def __init__(self, map_: SparseMap):
        hallway = []
        target_rooms = []

        self.map_ = map_

        for y in map_.rows:
            for x in map_.columns:
                if map_[x, y] in '.':
                    hallway.append((x, y))

                if map_[x, y] in 'ABCD':
                    target_rooms.append((x, y))

        self.target_rooms_by_type = defaultdict(list)
        for t, square in zip(cycle('DCBA'), reversed(target_rooms)):
            self.target_rooms_by_type[t].append(square)

        self.state_encoder = hallway + target_rooms
        print("Initial state")
        self.map_.print()
        self.initial_state = self.encode_state()

        for t, squares in self.target_rooms_by_type.items():
            for x, y in squares:
                self.map_[x, y] = t

        self.final_state = self.encode_state()
        print("Final state")
        self.map_.print()
        self.decode_state(self.initial_state)
        self.hallway = 1
        self.room_top = 2
        self.room_bottom = self.map_.rows - 2

    def placed(self, t, x, y) -> bool:
        if target_rooms[t] != x:
            return False

        for ny in interval(y, self.room_bottom):
            if self.map_[x, ny] != t:
                return False

        return True

    def encode_state(self) -> str:
        rv = ''
        for x, y in self.state_encoder:
            rv += self.map_[x, y]
        return rv

    def decode_state(self, state: str) -> None:
        for c, (x, y) in zip(state, self.state_encoder):
            self.map_[x, y] = c

        self.targettable_rooms = set('ABCD')
        for t, c in self.target_rooms_by_type.items():
            allowed = (t, '.')
            for x, y in c:
                if self.map_[x, y] not in allowed:
                    self.targettable_rooms.remove(t)
                    break


def part1(d: Input, ans: Answers) -> None:
    the_map = SparseMap(d.lines, default=' ')
    state_generator = StateGenerator(the_map)
    target_room_coords = set(target_rooms.values())

    def target_room_available(a: Amphipod):
        t = a.t
        room_x = target_rooms[t]
        for y in interval(state_generator.room_top, state_generator.room_bottom):
            if the_map[room_x, y] not in ('.', t):
                return False

        return True

    def generate_targets(a: Amphipod):
        move_cost = move_costs[a.t]
        room_x = target_rooms[a.t]

        can_move_to_room = target_room_available(a)
        hall_y = state_generator.hallway

        if not a.in_hallway:
            # blocked in room
            for i in interval(hall_y, a.y - 1):
                if the_map[a.x, a.y - 1] != '.':
                    return

            # and the_map[a.x, hall_y] == '.' true because hallway kept clear
            cur_cost = hall_cost = a.y - hall_y
            hall_x = a.x - 1

            possible = []
            while the_map[hall_x, hall_y] == '.':
                cur_cost += 1
                if can_move_to_room and hall_x == room_x:
                    # Find first available slot and generate move only there
                    for room_y in interval(state_generator.room_bottom,
                                           state_generator.room_top, -1):
                        if the_map[hall_x, room_y] == '.':
                            yield (
                                (
                                        cur_cost + room_y -
                                        state_generator.hallway) *
                                move_cost,
                                dataclasses.replace(
                                    a, x=hall_x, y=room_y
                                )
                            )
                            # IMMEDIATELY return
                            return

                # otherwise queue these moves; do not yield if we can get to
                # room
                elif hall_x not in target_room_coords:
                    possible.append((
                        cur_cost * move_cost,
                        dataclasses.replace(a, x=hall_x, y=hall_y)
                    ))

                hall_x -= 1

            cur_cost = hall_cost
            hall_x = a.x + 1
            while the_map[hall_x, hall_y] == '.':
                cur_cost += 1
                if can_move_to_room and hall_x == room_x:
                    for room_y in interval(
                            state_generator.room_bottom,
                            state_generator.room_top,
                            -1
                    ):
                        if the_map[hall_x, room_y] == '.':
                            yield (
                                (cur_cost + room_y - state_generator.hallway)
                                * move_cost,
                                dataclasses.replace(
                                    a, x=hall_x, y=room_y
                                )
                            )
                            # IMMEDIATELY return
                            return

                elif hall_x not in target_room_coords:
                    possible.append((
                        cur_cost * move_cost,
                        dataclasses.replace(a, x=hall_x, y=hall_y)
                    ))

                hall_x += 1

            yield from possible
            return

        if not can_move_to_room or not a.in_hallway:
            return

        dx = [-1, 1][room_x > a.x]
        current_x = a.x + dx
        cost = 1
        while current_x != room_x:
            if the_map[current_x, hall_y] != '.':
                return

            current_x += dx
            cost += 1

        for room_y in interval(
                state_generator.room_bottom,
                state_generator.room_top, -1
        ):
            if the_map[room_x, room_y] == '.':
                cost += room_y - state_generator.hallway

                yield (
                    cost * move_cost,
                    dataclasses.replace(
                        a, x=room_x, y=room_y
                    ))

    def generate_moves(state: str) -> Iterator[Tuple[int, int, str]]:
        state_generator.decode_state(state)

        amphipods = []
        map_ = state_generator.map_
        for x, y in state_generator.state_encoder:
            if (t := map_[x, y]) in 'ABCD':
                # we do not need to move placed amphipods any more
                if state_generator.placed(t, x, y):
                    continue

                amphipods.append(Amphipod(t, x, y, in_hallway=y == 1))

        heuristic = sum(min_energy_to_solve(a) for a in amphipods)
        for a in amphipods:
            to_solve_me = min_energy_to_solve(a)
            the_map[a.x, a.y] = '.'

            heuristic -= to_solve_me
            for new_cost, new_a in generate_targets(a):
                the_map[new_a.x, new_a.y] = a.t
                yield (
                    heuristic + min_energy_to_solve(a),
                    new_cost,
                    state_generator.encode_state()
                )
                the_map[new_a.x, new_a.y] = '.'

            heuristic += to_solve_me
            the_map[a.x, a.y] = a.t

    dist, target = a_star_solve(
        origin=state_generator.initial_state,
        target=state_generator.final_state,
        neighbours=generate_moves,
        integrated_heuristic=True
    )
    ans.part1 = dist

    l = list(d.lines)
    l[3:3] = [
        '  #D#C#B#A#',
        '  #D#B#A#C#',
    ]

    min_energy_to_solve.cache_clear()
    the_map = SparseMap(l, default=' ')
    state_generator = StateGenerator(the_map)

    dist2, target = a_star_solve(
        origin=state_generator.initial_state,
        target=state_generator.final_state,
        neighbours=generate_moves,
        integrated_heuristic=True
    )
    ans.part2 = dist2


run([1, 2], day=23, year=2021, submit=True)

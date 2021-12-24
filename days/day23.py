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
test_case(2, test_data, ...)


@dataclasses.dataclass(frozen=True, slots=True)
class Amphipod:
    t: str
    x: int
    y: int
    turns: int = 0
    placed: bool = False


target_rooms = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9
}


@lru_cache(maxsize=None)
def min_energy_to_solve(a: Amphipod):
    if a.placed:
        return 0
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


def part1(d: Input, ans: Answers) -> None:
    the_map = SparseMap(d.lines, default=' ')

    amphipods = []
    for y in the_map.rows:
        for x in the_map.columns:
            if the_map[x, y] in 'ABCD':
                amphipods.append(a := Amphipod(the_map[x, y], x, y))

    target_room_coords = set(target_rooms.values())

    min_cost = 100000000000000000000000
    hall_y = 1
    room_upper = 2
    room_lower = 3

    for i, a in enumerate(amphipods):
        if a.x == target_rooms[a.t] and the_map[a.x, 3] == a.t:
            amphipods[i] = dataclasses.replace(a, placed=True)

    def is_solved():
        return sum(a.placed for a in amphipods) == 8

    def n_placed():
        return sum(a.placed for a in amphipods)

    def target_room_available(a: Amphipod):
        t = a.t
        room_x = target_rooms[t]
        if (the_map[room_x, room_upper] in ('.', t)
                and the_map[room_x, room_lower] in ('.', t)):
            return True

        return False

    def generate_targets(a: Amphipod):
        move_cost = move_costs[a.t]
        room_x = target_rooms[a.t]

        can_move_to_room = target_room_available(a)

        if a.turns == 0 and the_map[a.x, a.y - 1] == '.':  # and the_map[a.x,
            # hall_y] == '.' true because hallway kept clear
            cur_cost = hall_cost = a.y - hall_y
            hall_x = a.x - 1

            while the_map[hall_x, hall_y] == '.':
                cur_cost += 1
                if can_move_to_room and hall_x == room_x:
                    if the_map[hall_x, room_lower] == '.':
                        yield (cur_cost + 2) * move_cost, dataclasses.replace(
                            a, x=hall_x, y=room_lower, turns=1, placed=True
                        )
                    else:
                        yield (cur_cost + 1) * move_cost, dataclasses.replace(
                            a, x=hall_x, y=room_upper, turns=1, placed=True
                        )
                elif hall_x not in target_room_coords:
                    yield cur_cost * move_cost, dataclasses.replace(
                        a, x=hall_x, y=hall_y, turns=1
                    )

                hall_x -= 1

            cur_cost = hall_cost
            hall_x = a.x + 1
            while the_map[hall_x, hall_y] == '.':
                cur_cost += 1
                if can_move_to_room and hall_x == room_x:
                    if the_map[hall_x, room_lower] == '.':
                        yield (cur_cost + 2) * move_cost, dataclasses.replace(
                            a, x=hall_x, y=room_lower, turns=1, placed=True
                        )
                    else:
                        yield (cur_cost + 1) * move_cost, dataclasses.replace(
                            a, x=hall_x, y=room_upper, turns=1, placed=True
                        )
                elif hall_x not in target_room_coords:
                    yield (
                        cur_cost * move_cost,
                        dataclasses.replace(a, x=hall_x, y=hall_y, turns=1)
                    )

                hall_x += 1

            return

        if not can_move_to_room or a.turns == 0:
            return

        dx = [-1, 1][room_x > a.x]
        current_x = a.x + dx
        cost = 1
        while current_x != room_x and the_map[current_x, hall_y] == '.':
            current_x += dx
            cost += 1

        if current_x == room_x:
            cost += 1
            target_y = room_upper

            if the_map[room_x, room_lower] == '.':
                cost += 1
                target_y = room_lower

            yield cost * move_cost, dataclasses.replace(
                a, x=room_x, y=target_y, turns=2, placed=True
            )

    def recurse(cost):
        nonlocal min_cost

        if cost > min_cost:
            return

        if is_solved():
            if cost < min_cost:
                print('new min cost', cost)
                min_cost = cost

            return

        total_to_solve = sum(min_energy_to_solve(a) for a in amphipods)
        for i, a in enumerate(amphipods):
            to_solve_me = min_energy_to_solve(a)
            if a.placed:
                continue

            the_map[a.x, a.y] = '.'

            total_to_solve -= to_solve_me
            for new_cost, new_a in generate_targets(a):
                if cost + total_to_solve + min_energy_to_solve(new_a) > min_cost:
                    continue

                the_map[new_a.x, new_a.y] = a.t
                amphipods[i] = new_a
                recurse(cost + new_cost)

                the_map[new_a.x, new_a.y] = '.'

            total_to_solve += to_solve_me
            amphipods[i] = a
            the_map[a.x, a.y] = a.t

    recurse(0)
    ans.part1 = min_cost


def part2(d: Input, ans: Answers) -> None:
    ...


run([1], day=23, year=2021, submit=True)

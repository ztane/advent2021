from helpers import *

test_data = Input("""
Player 1 starting position: 4
Player 2 starting position: 8
""")

test_case(1, test_data, 739785)
test_case(2, test_data, 444356092776315)

debug = False


@dataclasses.dataclass(frozen=True)
class UniverseState:
    player_pos: Tuple[int, int]
    player_score: Tuple[int, int]

    def move(self, player: int, dice: int):
        pos = list(self.player_pos)
        score = list(self.player_score)

        pos[player] = (pos[player] + dice) % 10
        score[player] += pos[player] + 1

        return UniverseState(tuple(pos), tuple(score))

    def winning(self):
        return any(i >= 21 for i in self.player_score)


def part1_and_2(d: Input, ans: Answers) -> None:
    start_pos = [0] * 2
    scores = [0] * 2
    rolls = 0
    _, start_pos[0], _, start_pos[1] = d.extract_ints
    dice_iterator = cycle(interval(1, 100))

    pos = start_pos.copy()

    def dice():
        nonlocal rolls
        rolls += 3
        return next(dice_iterator) + next(dice_iterator) + next(dice_iterator)

    i = 0
    won = False
    while not won:
        for i in interval(0, 1):
            move = dice()
            pos[i] += move
            pos[i] = (pos[i] - 1) % 10 + 1
            scores[i] += pos[i]

            if debug:
                print(f'player {i+1} moves to {pos[i]} for {scores[i]}')
            if scores[i] >= 1000:
                if debug:
                    print('player', i + 1, 'wins with', scores[i], 'points')

                ans.part1 = scores[not i] * rolls
                won = True
                break

    pos = [i - 1 for i in start_pos]
    uni_counts = Counter[UniverseState]()
    starting = UniverseState(tuple(pos), (0, 0))
    uni_counts[starting] = 1
    wins = Counter()
    moves = list({3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}.items())

    while True:
        if not uni_counts:
            break

        for player in interval(0, 1):
            new_uni_counts: Counter[UniverseState] = Counter()
            for universe_state, u_count in uni_counts.items():
                for dice, ct in moves:
                    new_state = universe_state.move(player, dice)
                    if new_state.winning():
                        wins[player] += u_count * ct
                    else:
                        new_uni_counts[new_state] += u_count * ct

            uni_counts = new_uni_counts

    ans.part2 = max(wins.values())


run([1, 2], day=21, year=2021, submit=True)

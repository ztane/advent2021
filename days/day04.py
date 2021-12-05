from helpers import *

test_data = Data("""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""")

test_case(1, test_data, 4512)
test_case(2, test_data, 1924)


def part1_and_2(d: Data, ans: Answers) -> None:
    numbers: Data
    boards: Tuple[Data]
    numbers, *boards = d.split('\n\n')
    numbers_as_list = numbers.extract_ints

    boards_as_lists = []
    for b in boards:
        boards_as_lists.append(list(b.extract_ints))

    def check_win(board, loc):
        y, x = loc // 5, loc % 5

        hor_win = True
        vert_win = True
        for c in range(5):
            if board[c + y * 5]:
                hor_win = False
            if board[c * 5 + x]:
                vert_win = False

        return hor_win or vert_win

    for i in numbers_as_list:
        for b in list(boards_as_lists):
            try:
                loc = b.index(i)
                b[loc] = 0
                if check_win(b, loc):
                    if ans.part1 is None:
                        ans.part1 = sum(b) * i

                    ans.part2 = sum(b) * i
                    boards_as_lists.remove(b)

            except:
                pass


run([1, 2], day=4, year=2021, submit=True)

from helpers import *

test_case(1, "8A004A801A8002F478", 16)
test_case(1, "C0015000016115A2E0802F182340", 23)
test_case(1, "620080001611562C8802118E34", 12)
test_case(1, "A0016C880162017C3686B18A3D4780", 31)
test_case(2, 'C200B40A82', 3)
test_case(2, '04005AC33890', 54)
test_case(2, '880086C3E88112', 7)
test_case(2, 'CE00C43D881120', 9)
test_case(2, 'D8005AC2A8F0', 1)
test_case(2, 'F600BC2D8F', 0)
test_case(2, '9C005AC2F8F0', 0)
test_case(2, '9C0141080250320F1802104A08', 1)


def part1_and_2(d: Input, ans: Answers) -> None:
    bits = f'{int("1" + d, 16):b}'[1:]
    pos = 0

    def take1():
        nonlocal pos
        rv = bits[pos]
        pos += 1
        return rv

    def take(n):
        bitstring = ''.join(take1() for _ in range(n))
        return int(bitstring, 2)

    def evaluate() -> Tuple[int, int]:
        v = take(3)
        t = take(3)
        if t == 4:
            more = 1

            val = 0
            while more:
                more = take(1)
                valbits = take(4)
                val <<= 4
                val |= valbits

            return v, val

        vals = []

        length_type = take(1)
        if length_type:
            num_packets = take(11)
            for i in range(num_packets):
                vers, val = evaluate()
                v += vers
                vals.append(val)

        else:
            packet_bits = take(15)
            endpos = pos + packet_bits
            while pos < endpos:
                vers, val = evaluate()
                v += vers
                vals.append(val)

            assert endpos == pos

        match t:
            case 0: rv = sum(vals)
            case 1: rv = prod(vals)
            case 2: rv = min(vals)
            case 3: rv = max(vals)
            case 5: rv = int(vals[0] > vals[1])
            case 6: rv = int(vals[0] < vals[1])
            case 7: rv = int(vals[0] == vals[1])
            case _:
                raise Exception("Unknown operator")

        return v, rv

    ans.part1, ans.part2 = evaluate()


run([1, 2], day=16, year=2021, submit=True)

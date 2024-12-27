import os.path
import re
from collections import deque

DATA = os.path.join(os.path.dirname(__file__), 'day24.txt')


def __build_wires_and_gates(data) -> tuple:
    lines = data.splitlines()
    wires = {}
    gates_idx = -1

    for i in range(len(lines)):
        if lines[i] == "":
            gates_idx = i + 1
            break

        parts = lines[i].split(": ")
        wires[parts[0]] = int(parts[1])

    return wires, deque(lines[gates_idx:])

def __build_gates(data) -> dict:
    lines = data.splitlines()
    operations = {}
    gates_idx = -1

    for i in range(len(lines)):
        if lines[i] == "":
            gates_idx = i + 1
            break

    for l in lines[gates_idx:]:
        (l, op, r, dest_wire) = re.findall(r'([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})', l)[0]
        operations[(l, op, r)] = dest_wire

    return operations


def __is_input_wire(wire) -> bool:
    return wire.startswith('x') or wire.startswith('y')


def __are_inputs_first_bits(w1, w2) -> bool:
    return w1.endswith("00") and w2.endswith("00")

def part_one(data) -> int:
    wires, gates = __build_wires_and_gates(data)
    answer = ""

    while len(gates) != 0:
        gate = gates.popleft()
        (l, op, r, dest_wire) = re.findall(r'([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})', gate)[0]
        if l not in wires or r not in wires:
            gates.append(gate)
            continue

        if op == "AND":
            wires[dest_wire] = wires[l] & wires[r]
        elif op == "OR":
            wires[dest_wire] = wires[l] | wires[r]
        else:
            wires[dest_wire] = wires[l] ^ wires[r]

    sorted_wires = dict(sorted(wires.items()))
    for k, v in sorted_wires.items():
        if k[0] == 'z':
            answer = str(v) + answer

    return int(answer, 2)


# Inspiration from:
# https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3lnhrw/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# https://github.com/Gmark2000/advent-of-code-2024-MarkGozner/blob/main/Day24/Program.cs#L112
def part_two(data) -> str:
    gates = __build_gates(data)
    faulty_gates = []

    for k, v in gates.items():
        left, op, right = k
        dest = v
        is_faulty = False

        if dest.startswith('z') and dest != "z45":
            is_faulty = op != "XOR"
        elif not dest.startswith('z') and not __is_input_wire(left) and not __is_input_wire(right):
            is_faulty = op == "XOR"
        elif __is_input_wire(left) and __is_input_wire(right) and not __are_inputs_first_bits(left, right):
            if op == "XOR":
                expected_next_type = "XOR"
            else:
                expected_next_type = "OR"

            feeds = False
            for kk, vv in gates.items():
                if kk == k:
                    continue

                other_left, other_op, other_right = kk
                if (other_left == dest or other_right == dest) and other_op == expected_next_type:
                    feeds = True
                    break

            is_faulty = not feeds

        if is_faulty:
            faulty_gates.append(dest)

    return ",".join(sorted(faulty_gates))


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        # print("Part 1: " + str(part_one(data)))
        print("Part 2: " + part_two(data))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


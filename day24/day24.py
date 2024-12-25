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

def __build_operation_tree(data) -> dict:
    lines = data.splitlines()
    operations = {}
    gates_idx = -1

    for i in range(len(lines)):
        if lines[i] == "":
            gates_idx = i + 1
            break

    for l in lines[gates_idx:]:
        (l, op, r, dest_wire) = re.findall(r'([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})', l)[0]
        operations[(l, r)] = dest_wire

    return operations


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


def part_two(data) -> str:
    return ""


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + part_two(data))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


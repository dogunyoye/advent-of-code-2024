import os.path
from itertools import combinations

DATA = os.path.join(os.path.dirname(__file__), 'day08.txt')


def __print_grid(grid):
    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            line += grid[(i, j)]
        print(line)


def __build_map(data) -> dict:
    i = 0
    grid = {}
    for line in data.splitlines():
        for j, c in enumerate(line):
            grid[(i, j)] = c
        i += 1
    return grid


def __antennas_map(grid) -> dict:
    antennas_map = {}
    for k, v in grid.items():
        if v != '.':
            if v in antennas_map:
                antennas_map[v].append(k)
            else:
                antennas_map[v] = [k]
    return antennas_map


def part_one(data) -> int:
    grid = __build_map(data)
    antennas = __antennas_map(grid)
    antinodes = set()

    for v in antennas.values():
        for c in list(combinations(v, 2)):
            a0, a1 = c[0], c[1]
            dx, dy = a0[0] - a1[0], a0[1] - a1[1]
            antinodes.add((a0[0] + dx, a0[1] + dy))
            antinodes.add((a1[0] - dx, a1[1] - dy))

    max_i = max(grid, key=lambda x: x[0])[0]
    max_j = max(grid, key=lambda x: x[1])[1]
    antinodes = set(filter(lambda x: 0 <= x[0] <= max_i and 0 <= x[1] <= max_j, antinodes))

    return len(antinodes)


def part_two(data) -> int:
    grid = __build_map(data)
    antennas = __antennas_map(grid)
    antinodes = set()
    max_i = max(grid, key=lambda x: x[0])[0]
    max_j = max(grid, key=lambda x: x[1])[1]

    for v in antennas.values():
        for c in list(combinations(v, 2)):
            a0, a1 = c[0], c[1]
            dx, dy = a0[0] - a1[0], a0[1] - a1[1]
            while 0 <= a0[0] + dx <= max_i and 0 <= a0[1] + dy <= max_j:
                a0 = (a0[0] + dx, a0[1] + dy)
                antinodes.add(a0)
            while 0 <= a1[0] - dx <= max_i and 0 <= a1[1] - dy <= max_j:
                a1 = (a1[0] - dx, a1[1] - dy)
                antinodes.add(a1)

    for v in antennas.values():
        for a in v:
            antinodes.add(a)

    return len(antinodes)


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

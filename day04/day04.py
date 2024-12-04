import os.path
from collections import Counter

DATA = os.path.join(os.path.dirname(__file__), 'day04.txt')


def __print_grid(grid):
    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            line += grid[(i, j)]
        print(line)


def __build_wordsearch_grid(data) -> dict:
    grid = {}
    i = 0
    for line in data.splitlines():
        for j, c in enumerate(line):
            grid[(i, j)] = c
        i += 1
    return grid


def __check_coord(coord, grid, dx, dy) -> str:
    xmas = ""
    for p in range(4):
        point = (coord[0] + (p * dx), coord[1] + (p * dy))
        if point in grid:
            xmas += grid[point]
    return xmas


def __find_xmas(coord, grid) -> int:
    result = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if __check_coord(coord, grid, dx, dy) == "XMAS":
                result += 1
    return result


def __find_xmas_properly(coord, grid) -> int:
    xmas = ""
    ne = (coord[0] - 1, coord[1] + 1)
    se = (coord[0] + 1, coord[1] + 1)
    sw = (coord[0] + 1, coord[1] - 1)
    nw = (coord[0] - 1, coord[1] - 1)

    if ne in grid:
        xmas += grid[ne]

    if se in grid:
        xmas += grid[se]

    if sw in grid:
        xmas += grid[sw]

    if nw in grid:
        xmas += grid[nw]

    c = Counter(xmas)
    if c['S'] == 2 and c['M'] == 2 and (grid[nw] == grid[ne] or grid[ne] == grid[se]):
        return 1
    return 0


def part_one(data) -> int:
    grid = __build_wordsearch_grid(data)
    result = 0
    for k, v in grid.items():
        if v == 'X':
            result += __find_xmas(k, grid)
    return result


def part_two(data) -> int:
    grid = __build_wordsearch_grid(data)
    result = 0
    for k, v in grid.items():
        if v == 'A':
            result += __find_xmas_properly(k, grid)
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

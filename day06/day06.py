import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day06.txt')


def __print_grid(grid):
    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            line += grid[(i, j)]
        print(line)


def __build_map(data) -> (dict, tuple):
    i = 0
    grid = {}
    start = (-1, -1)
    for line in data.splitlines():
        for j, c in enumerate(line):
            grid[(i, j)] = c
            if c == '^':
                start = (i, j)
        i += 1
    return grid, start


def __turn(facing) -> chr:
    if facing == '^':
        return '>'
    if facing == '>':
        return 'v'
    if facing == 'v':
        return '<'
    if facing == '<':
        return '^'


def __move(position, grid) -> tuple:
    facing = grid[position]
    next_position = (-1, -1)
    if facing == '^':
        next_position = (position[0] - 1, position[1])
    if facing == '>':
        next_position = (position[0], position[1] + 1)
    if facing == 'v':
        next_position = (position[0] + 1, position[1])
    if facing == '<':
        next_position = (position[0], position[1] - 1)

    if next_position in grid and grid[next_position] == '#':
        grid[position] = __turn(facing)
        return position

    grid[position] = '.'
    if next_position in grid:
        grid[next_position] = facing

    return next_position


def __simulate_patrol(grid, current_position) -> set:
    positions = set()
    unique_positions = set()

    while current_position in grid:
        positions.add((current_position, grid[current_position]))
        current_position = __move(current_position, grid)

    for p in positions:
        unique_positions.add(p[0])

    return unique_positions


def __loop_found(grid, current_position) -> bool:
    positions = set()
    while current_position in grid:
        if current_position in grid and (current_position, grid[current_position]) in positions:
            return True
        positions.add((current_position, grid[current_position]))
        current_position = __move(current_position, grid)
    return False


def part_one(data) -> int:
    grid, current_position = __build_map(data)
    return len(__simulate_patrol(grid, current_position))


def part_two(data) -> int:
    grid, current_position = __build_map(data)
    open_positions = __simulate_patrol(grid, current_position)
    open_positions.remove(current_position)
    loops = 0

    for p in open_positions:
        grid, current_position = __build_map(data)
        grid[p] = '#'
        if __loop_found(grid, current_position):
            loops += 1

    return loops


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

import os.path
from collections import deque

DATA = os.path.join(os.path.dirname(__file__), 'day10.txt')


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
    starts = []
    for line in data.splitlines():
        for j, c in enumerate(line):
            grid[(i, j)] = c
            if c == '0':
                starts.append((i, j))
        i += 1
    return grid, starts


def __bfs(grid, start) -> int:
    queue, visited = deque(), set()
    queue.append(start)
    score = 0

    while len(queue) != 0:
        current_position = queue.popleft()
        i, j = current_position[0], current_position[1]
        level = grid[current_position]

        if level == '9':
            score += 1
            continue

        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]
        for n in neighbors:
            if n in grid and grid[n] != '.' and n not in visited and int(grid[n]) == int(level) + 1:
                queue.append(n)
                visited.add(n)

    return score


def __dfs(grid, start) -> int:
    stack = [start]
    score = 0

    while len(stack) != 0:
        current_position = stack.pop()
        i, j = current_position[0], current_position[1]
        level = grid[current_position]

        if level == '9':
            score += 1
            continue

        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]
        for n in neighbors:
            if n in grid and grid[n] != '.' and int(grid[n]) == int(level) + 1:
                stack.append(n)

    return score


def part_one(data) -> int:
    grid, starts = __build_map(data)
    result = 0
    for s in starts:
        result += __bfs(grid, s)
    return result


def part_two(data) -> int:
    grid, starts = __build_map(data)
    result = 0
    for s in starts:
        result += __dfs(grid, s)
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

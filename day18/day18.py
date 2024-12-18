import os.path
from collections import deque

DATA = os.path.join(os.path.dirname(__file__), 'day18.txt')

BOUND = 70


def __print_grid(grid):
    for y in range(BOUND + 1):
        line = ""
        for x in range(BOUND + 1):
            line += grid[(x, y)]
        print(line)


def __build_falling_bytes_list(data) -> list:
    falling_bytes = []
    for line in data.splitlines():
        xy = line.split(",")
        (x, y) = int(xy[0]), int(xy[1])
        falling_bytes.append((x, y))
    return falling_bytes


def __initialise_grid() -> dict:
    grid = {}
    for y in range(BOUND + 1):
        for x in range(BOUND + 1):
            grid[(x, y)] = '.'
    return grid


def __bfs(start, end, grid) -> tuple:
    queue, visited = deque(), set()
    path = set()
    path.add(start)
    queue.append((start, 0, path))

    while len(queue) != 0:
        current = queue.popleft()
        (x, y), steps, path = current[0], current[1], current[2]

        if (x, y) == end:
            return steps, path

        neighbors = [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]
        for n in neighbors:
            if n in grid and grid[n] != '#' and n not in visited:
                new_path = set(path)
                new_path.add(n)
                queue.append((n, steps + 1, new_path))
                visited.add(n)

    return -1, set()


def part_one(data) -> int:
    falling_bytes = __build_falling_bytes_list(data)
    grid = __initialise_grid()

    for f in falling_bytes[0:1024]:
        grid[f] = '#'

    return __bfs((0, 0), (BOUND, BOUND), grid)[0]


def part_two(data) -> str:
    falling_bytes = __build_falling_bytes_list(data)
    grid = __initialise_grid()

    for f in falling_bytes[0:1024]:
        grid[f] = '#'

    _, path = __bfs((0,0), (BOUND, BOUND), grid)

    for i in range(1024, len(falling_bytes)):
        grid[falling_bytes[i]] = '#'
        if falling_bytes[i] in path:
            steps, path = __bfs((0,0), (BOUND, BOUND), grid)
            if steps == -1:
                return str(falling_bytes[i])

    raise Exception("No solution found!")


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

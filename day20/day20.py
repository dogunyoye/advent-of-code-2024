import os.path
from collections import deque, defaultdict

DATA = os.path.join(os.path.dirname(__file__), 'day20.txt')


def __print_grid(grid):
    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            line += grid[(i, j)]
        print(line)


def __build_racetrack(data) -> tuple:
    grid = {}
    start = (-1, -1)
    end = (-1, -1)
    i = 0
    for line in data.splitlines():
        for j, c in enumerate(line):
            grid[(i, j)] = c
            if c == 'S':
                start = (i, j)
            elif c == 'E':
                end = (i, j)
        i += 1
    return grid, start, end


def manhattan_distance(point1, point2):
    # Calculate the Manhattan distance between two points
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def __bfs(grid, start, end, track_walls) -> tuple:
    queue, visited = deque(), set()
    queue.append((start, 0, set(), []))

    while len(queue) != 0:
        current_position = queue.popleft()
        i, j = current_position[0]
        steps = current_position[1]
        walls = current_position[2]
        path = current_position[3]

        if current_position[0] == end:
            return steps, walls, path

        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]
        if track_walls:
            next_walls = set(walls)
            for n in neighbors:
                if n in grid and grid[n] == '#':
                    next_walls.add(n)
        else :
            next_walls = set()

        for n in neighbors:
            if n in grid and grid[n] != '#' and n not in visited:
                new_path = list(path)
                new_path.append(n)
                queue.append((n, steps + 1, next_walls, new_path))
                visited.add(n)

    raise Exception("No solution!")


def __bfs_constrained(grid, start, end, limit) -> int:
    queue, visited = deque(), set()
    queue.append((start, 0))

    while len(queue) != 0:
        current_position = queue.popleft()
        i, j = current_position[0]
        steps = current_position[1]

        if steps >= limit:
            continue

        if current_position[0] == end:
            return steps

        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]
        for n in neighbors:
            if n in grid and grid[n] != '#' and n not in visited:
                queue.append((n, steps + 1))
                visited.add(n)

    return -1


def __bfs_move_through_walls(grid, start, end, saving, limit):
    queue, visited = deque(), set()
    cheat_start, cheat_end = (-1, -1), (-1, -1)
    queue.append((start, cheat_start, cheat_end, 0, 20))
    visited.add((start, cheat_start, cheat_end))

    while len(queue) != 0:
        current_position = queue.popleft()
        i, j = current_position[0]
        cheat_start, cheat_end = current_position[1], current_position[2]
        steps = current_position[3]
        wall_moves = current_position[4]

        if steps >= limit:
            continue

        if current_position[0] == end:
            saving[((limit - steps), cheat_start, cheat_end)] += 1
            print(saving)
            continue

        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]

        for n in neighbors:
            if n in grid and grid[n] == "#" and (n, cheat_start, cheat_end) not in visited:
                if wall_moves > 0:
                    if cheat_start == (-1, -1):
                        queue.append((n, (i, j), cheat_end, steps + 1, wall_moves - 1))
                        visited.add((n, (i, j), cheat_end))
                    else:
                        queue.append((n, cheat_start, cheat_end, steps + 1, wall_moves - 1))
                        visited.add((n, cheat_start, cheat_end))
            elif n in grid and grid[n] != "#" and (n, cheat_start, cheat_end) not in visited:
                if grid[(i, j)] == '#' and cheat_end == (-1, -1):
                    queue.append((n, cheat_start, n, steps + 1, wall_moves - 1))
                    visited.add((n, cheat_start, n))
                else:
                    if cheat_start == (-1, -1):
                        queue.append((n, cheat_start, cheat_end, steps + 1, wall_moves))
                    else:
                        queue.append((n, cheat_start, cheat_end, steps + 1, wall_moves - 1))
                    visited.add((n, cheat_start, cheat_end))


def part_one(data) -> int:
    racetrack, start, end = __build_racetrack(data)
    saving = defaultdict(int)
    original_score, walls, path = __bfs(racetrack, start, end, True)

    for w in walls:
        racetrack[w] = '.'
        new_score = __bfs_constrained(racetrack, start, end, original_score)
        if new_score != -1:
            saving[(original_score - new_score)] += 1
        racetrack[w] = '#'

    result = 0
    for k, v in saving.items():
        if k >= 100:
            result += v

    return result


def part_two(data) -> int:
    racetrack, start, end = __build_racetrack(data)
    saving = defaultdict(int)
    original_score, _ = __bfs(racetrack, start, end, False)

    __bfs_move_through_walls(racetrack, start, end, saving, original_score)

    result = 0
    print(saving)
    for k, v in saving.items():
        if k[0] == 74:
            print((k, v))
            result += 1

    return result

def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        # print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


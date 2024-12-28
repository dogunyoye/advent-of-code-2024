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
    queue.append((start, 0, set(), {(start, 0)}))

    while len(queue) != 0:
        current_position = queue.popleft()
        i, j = current_position[0]
        steps = current_position[1]
        walls = current_position[2]
        path = current_position[3]

        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]
        if track_walls:
            next_walls = set(walls)
            for n in neighbors:
                if n in grid and grid[n] == '#':
                    next_walls.add((n, steps))
        else :
            next_walls = set()

        if current_position[0] == end:
            return steps, walls, path

        for n in neighbors:
            if n in grid and grid[n] != '#' and n not in visited:
                new_path = set(path)
                new_path.add((n, steps + 1))
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


def part_one(data) -> int:
    racetrack, start, end = __build_racetrack(data)
    saving = defaultdict(int)
    original_score, walls, path = __bfs(racetrack, start, end, True)

    for w, step in walls:
        i, j = w
        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]
        count = 0

        for n in neighbors:
            if n in racetrack and racetrack[n] != '#' and len([p for p in path if p[0] == n]) > 0:
                count += 1

        if count > 1:
            racetrack[w] = '.'
            new_score = __bfs_constrained(racetrack, w, end, original_score)
            if new_score != -1:
                saving[(original_score - (new_score + step + 1))] += 1
            racetrack[w] = '#'

    result = 0
    for k, v in saving.items():
        if k >= 100:
            result += v

    return result


def part_two(data) -> int:
    racetrack, start, end = __build_racetrack(data)
    saving = defaultdict(int)
    original_score, _, path= __bfs(racetrack, start, end, False)

    for a, a_step in path:
        for b, b_step in path:
            if a == b:
                continue
            dist = manhattan_distance(a, b)
            dist_start_end = original_score - a_step
            cheat_way = dist + (original_score - b_step)
            if dist <= 20:
                saved = dist_start_end - cheat_way
                if saved >= 100:
                    saving[saved] += 1

    result = 0
    for k, v in saving.items():
        result += v

    return result

def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

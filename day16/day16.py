import os.path
import heapq
import sys
from heapq import heappop

DATA = os.path.join(os.path.dirname(__file__), 'day16.txt')


def __print_grid(grid):
    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            line += grid[(i, j)]
        print(line)


def __print_grid_with_path(grid, path):
    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            if (i, j) in path:
                line += '*'
            else:
                line += grid[(i, j)]
        print(line)


def __build_map(data) -> (dict, tuple):
    i = 0
    grid = {}
    start, end = (-1, -1), (-1, -1)
    for line in data.splitlines():
        for j, c in enumerate(line):
            grid[(i, j)] = c
            if c == 'S':
                start = (i, j)
            if c == 'E':
                end = (i, j)
        i += 1
    return grid, start, end


def __find_lowest_reindeer_score(grid, start, end) -> int:
    pq, distances, previous = [], {}, {}
    heapq.heappush(pq, (0, start, "east"))
    distances[start] = 0

    while len(pq) != 0:
        (current_score, current_position, facing) = heappop(pq)

        if current_position == end:
            return current_score

        if current_score > distances[current_position]:
            continue

        (i, j) = current_position
        neighbors = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)] # N E S W

        if facing == 'north':
            facing_idx = 0
        elif facing == 'east':
            facing_idx = 1
        elif facing == 'south':
            facing_idx = 2
        else:
            facing_idx = 3

        for idx, n in enumerate(neighbors):
            # map our next position to neighbours index
            if idx == 0:
                next_facing = "north"
            elif idx == 1:
                next_facing = "east"
            elif idx == 2:
                next_facing = "south"
            else:
                next_facing = "west"

            if n in grid and grid[n] != '#':
                next_score = current_score + 1
                if idx != facing_idx:
                    next_score += 1000
                if n not in distances or next_score < distances[n]:
                    distances[n] = next_score
                    previous[n] = current_position
                    heapq.heappush(pq, (next_score, n, next_facing))

    raise Exception("No solution found!")


def __find_all_best_paths(grid, start, end) -> int:
    pq, distances, all_paths = [], {}, []
    heapq.heappush(pq, (0, start, "east", [start]))
    distances[(start, "east")] = 0
    all_tiles = set()
    target = sys.maxsize

    while len(pq) != 0:
        (current_score, current_position, facing, path) = heappop(pq)
        if current_score > target:
            continue

        if current_position == end:
            target = min(target, current_score)
            if current_score == target:
                all_tiles.update(path)
            continue

        if current_score > distances[(current_position, facing)]:
            continue

        (i, j) = current_position
        neighbors = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)] # N E S W

        if facing == 'N':
            facing_idx = 0
        elif facing == 'E':
            facing_idx = 1
        elif facing == 'S':
            facing_idx = 2
        else:
            facing_idx = 3

        for idx, n in enumerate(neighbors):
            # map our next position to neighbours index
            if idx == 0:
                next_facing = "N"
            elif idx == 1:
                next_facing = "E"
            elif idx == 2:
                next_facing = "S"
            else:
                next_facing = "W"

            if n in grid and grid[n] != '#':
                next_score = current_score + 1
                if idx != facing_idx:
                    next_score += 1000
                if (n, next_facing) not in distances or next_score <= distances[(n, next_facing)]:
                    distances[(n, next_facing)] = next_score
                    heapq.heappush(pq, (next_score, n, next_facing, path + [n]))

    return len(all_tiles)

def part_one(data) -> int:
    grid, start, end = __build_map(data)
    return __find_lowest_reindeer_score(grid, start, end)


def part_two(data) -> int:
    grid, start, end = __build_map(data)
    return __find_all_best_paths(grid, start, end)


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


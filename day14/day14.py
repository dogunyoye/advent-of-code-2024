import os.path
import re
import sys

DATA = os.path.join(os.path.dirname(__file__), 'day14.txt')


def __print_grid(grid, max_x, max_y):
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            count = 0
            for v in grid.values():
                if (x, y) == v:
                    count += 1
            if count == 0:
                line += '.'
            else:
                line += str(count)
        print(line)


def __build_robots_map(data) -> (dict, dict, int, int):
    robots = {}
    velocities = {}
    robot_id = 0
    max_x, max_y = -sys.maxsize, -sys.maxsize

    for line in data.splitlines():
        (x, y, x_vel, y_vel) = re.findall(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)[0]
        robots[robot_id] = (int(x), int(y))
        velocities[robot_id] = (int(x_vel), int(y_vel))
        max_x = max(max_x, int(x))
        max_y = max(max_y, int(y))
        robot_id += 1

    return robots, velocities, max_x, max_y


def __move_robots(robots, velocities, seconds, max_x, max_y):
    for k, v in robots.items():
        (x_vel, y_vel) = velocities[k]
        robots[k] = (((v[0] + (seconds * x_vel)) % (max_x + 1)), ((v[1] + (seconds * y_vel)) % (max_y + 1)))


def part_one(data) -> int:
    (robots, velocities, max_x, max_y) = __build_robots_map(data)
    __move_robots(robots, velocities, 100, max_x, max_y)

    result = 1
    for xbound in [(0, (max_x / 2) - 1), ((max_x / 2) + 1, max_x)]:
        for ybound in [(0, (max_y / 2) - 1), ((max_y / 2) + 1, max_y)]:
            count = 0
            for v in robots.values():
                if xbound[0] <= v[0] <= xbound[1] and ybound[0] <= v[1] <= ybound[1]:
                    count += 1
            result *= count

    return result


def part_two(data) -> int:
    (robots, velocities, max_x, max_y) = __build_robots_map(data)
    seconds = 0

    while True:
        __move_robots(robots, velocities, 1, max_x, max_y)
        seconds += 1
        if len(set(robots.values())) == len(robots.keys()):
            return seconds


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

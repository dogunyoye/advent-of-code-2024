import os.path
from collections import deque

DATA = os.path.join(os.path.dirname(__file__), 'day12.txt')


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
    starts = set()
    for line in data.splitlines():
        for j, c in enumerate(line):
            grid[(i, j)] = c
            starts.add((i, j))
        i += 1
    return grid, starts


# Idea here is to:
# - build a bounding box around the region
# - look for the N,E,S,W neighbour for every point in the bounding box
# - if it directly touches the region, that position is next to a side
# - there could be numerous points touching the same side, so we want
# to reduce that region face to a single representative point
# - we do this by "sweeping" left/right or up/down to remove all but
# one point on the same line
# - at the end, for each direction (N, E, S, W) we will have a point per
# side => the number of slides for the entire region
def __calculate_number_of_sides(region) -> int:
    outer_region = set()
    neighbours = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    number_of_sides = 0

    for p in region:
        for n in neighbours:
            neighbour = (p[0] + n[0], p[1] + n[1])
            if neighbour not in region and neighbour not in outer_region:
                outer_region.add(neighbour)

    for idx, n in enumerate(neighbours):
        sides = []
        for p in outer_region:
            pn = (p[0] + n[0], p[1] + n[1])
            if pn in region:
                sides.append(p)

        side_regions = []

        if idx == 0 or idx == 2:  # (North or South) sweep left and right
            while len(sides) != 0:
                face_point = sides.pop()
                points = []
                sweep_left = (face_point[0], face_point[1] - 1)
                sweep_right = (face_point[0], face_point[1] + 1)
                points.append(face_point)

                while sweep_left in sides:
                    sides.remove(sweep_left)
                    sweep_left = (sweep_left[0], sweep_left[1] - 1)

                while sweep_right in sides:
                    sides.remove(sweep_right)
                    sweep_right = (sweep_right[0], sweep_right[1] + 1)

                side_regions.append(points)
        else:  # (East and West) sweep up and down
            while len(sides) != 0:
                face_point = sides.pop()
                points = []
                sweep_up = (face_point[0] - 1, face_point[1])
                sweep_down = (face_point[0] + 1, face_point[1])
                points.append(face_point)

                while sweep_up in sides:
                    sides.remove(sweep_up)
                    sweep_up = (sweep_up[0] - 1, sweep_up[1])

                while sweep_down in sides:
                    sides.remove(sweep_down)
                    sweep_down = (sweep_down[0] + 1, sweep_down[1])

                side_regions.append(points)

        number_of_sides += len(side_regions)

    return number_of_sides


def __cost_of_plot(grid, starts, is_part_two) -> int:
    queue, visited = deque(), set()
    start = starts.pop()
    queue.append(start)
    area, perimeter = 0, 0

    while len(queue) != 0:
        current_position = queue.popleft()
        i, j = current_position[0], current_position[1]
        area += 1

        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]
        for n in neighbors:
            if n in grid and n not in visited and grid[n] == grid[current_position]:
                queue.append(n)
                visited.add(n)
                if n in starts:
                    starts.remove(n)

    if area > 1:
        area -= 1
    else:
        return 4

    if is_part_two:
        return area * __calculate_number_of_sides(visited)

    for p in visited:
        i, j = p[0], p[1]
        p_perimiter = 4
        neighbors = [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]
        for n in neighbors:
            if n in visited:
                p_perimiter -= 1
        perimeter += p_perimiter

    return area * perimeter


def part_one(data) -> int:
    grid, starts = __build_map(data)
    result = 0
    while len(starts) != 0:
        result += __cost_of_plot(grid, starts, False)
    return result


def part_two(data) -> int:
    grid, starts = __build_map(data)
    result = 0
    while len(starts) != 0:
        result += __cost_of_plot(grid, starts, True)
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

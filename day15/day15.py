import os.path
from collections import deque


DATA = os.path.join(os.path.dirname(__file__), 'day15.txt')


def __print_grid(grid):
    max_i = max(grid, key=lambda x: x[0])
    max_j = max(grid, key=lambda x: x[1])
    for i in range(max_i[0] + 1):
        line = ""
        for j in range(max_j[1] + 1):
            line += grid[(i, j)]
        print(line)


def __build_grid_and_instructions(data) -> tuple:
    grid, instructions = {}, deque()
    lines = data
    start = (-1, -1)

    for i in range(len(lines)):
        if lines[i] == "":
            for j in range(i, len(lines)):
                for c in lines[j]:
                    instructions.append(c)
            break

        for j, c in enumerate(lines[i]):
            grid[(i, j)] = c
            if c == "@":
                start = (i, j)

    return grid, instructions, start


def __modified_grid(data) -> tuple:
    lines = data.splitlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("#", "##")
        lines[i] = lines[i].replace("O", "[]")
        lines[i] = lines[i].replace(".", "..")
        lines[i] = lines[i].replace("@", "@.")

    return __build_grid_and_instructions(lines)


def __find_boxes(grid) -> dict:
    boxes = {}
    for k, v in grid.items():
        if v == '[':
            boxes[k] = (k[0], k[1] + 1)
        elif v == ']':
            boxes[k] = (k[0], k[1] - 1)
    return boxes

def __move_robot(grid, instructions, start):
    current_position = start

    while len(instructions) != 0:
        movement = instructions.popleft()

        if movement == '^':
            dxdy = (-1, 0)
        elif movement == '>':
            dxdy = (0, 1)
        elif movement == 'v':
            dxdy = (1, 0)
        else:
            dxdy = (0, -1)

        next_position = (current_position[0] + dxdy[0], current_position[1] + dxdy[1])

        if grid[next_position] == '#':
            # print(movement)
            # __print_grid(grid)
            # print()
            continue

        if grid[next_position] == '.':
            grid[current_position] = '.'
            grid[next_position] = '@'
        elif grid[next_position] == 'O':
            next_item_position = (next_position[0] + dxdy[0], next_position[1] + dxdy[1])
            if grid[next_item_position] == '.':
                grid[next_item_position] = 'O'
                grid[next_position] = '@'
            elif grid[next_item_position] == 'O':
                pos = current_position
                shifts, space_available = 0, False

                while grid[pos] != '#':
                    if grid[pos] == '.':
                        space_available = True
                        break
                    pos = (pos[0] + dxdy[0], pos[1] + dxdy[1])
                    shifts += 1

                if not space_available:
                    # print(movement)
                    # __print_grid(grid)
                    # print()
                    continue

                # step back into last previously occupied position
                pos = (pos[0] + (-dxdy[0]), pos[1] + (-dxdy[1]))

                for _ in range(shifts):
                    val = grid[pos]
                    grid[(pos[0] + dxdy[0], pos[1] + dxdy[1])] = val
                    grid[pos] = '.'
                    pos = (pos[0] + (-dxdy[0]), pos[1] + (-dxdy[1]))
            else:
                # print(movement)
                # __print_grid(grid)
                # print()
                continue

        grid[current_position] = '.'
        current_position = next_position
        # print(movement)
        # __print_grid(grid)
        # print()


def part_one(data) -> int:
    grid, instructions, start = __build_grid_and_instructions(data.splitlines())
    __move_robot(grid, instructions, start)
    result = 0
    for k, v in grid.items():
        if v == 'O':
            result += ((100 * k[0]) + k[1])
    return result


def part_two(data) -> int:
    grid, instructions, start = __modified_grid(data)
    __print_grid(grid)
    print(__find_boxes(grid))
    return 0

def main() -> int:
    with open(DATA) as f:
        data = f.read()
        #print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

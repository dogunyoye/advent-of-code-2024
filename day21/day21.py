import itertools
import os.path
import sys
from collections import deque
from functools import lru_cache, cache
from itertools import permutations

DATA = os.path.join(os.path.dirname(__file__), 'day21.txt')


def __build_numerical_keypad() -> dict:
    return {
        (0, 0): '7', (0, 1): '8', (0, 2): '9',
        (1, 0): '4', (1, 1): '5', (1, 2): '6',
        (2, 0): '1', (2, 1): '2', (2, 2): '3',
        (3, 1): '0', (3, 2): 'A'
    }


def __build_directional_keypad() -> dict:
    return {
        (0, 1): '^', (0, 2): 'A',
        (1, 0): '<', (1, 1): 'v', (1, 2): '>',
    }


def __find_button_position(keypad_name, button) -> tuple:
    if keypad_name == "directional":
        keypad = __build_directional_keypad()
    else:
        keypad = __build_numerical_keypad()

    for k, v in keypad.items():
        if v == button:
            return k

    raise Exception("Button not found!")


def __option_valid(option, start, keypad_name) -> bool:
    i = 0
    current_position = start
    deltas = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

    if keypad_name == "numerical":
        banned = (3, 0)
    else:
        banned = (0, 0)

    while i != len(option):
        di, dj = deltas[option[i]]
        current_position = (current_position[0] + di, current_position[1] + dj)
        if current_position == banned:
            return False
        i += 1

    return True

def __bfs(keypad_name, start, end) -> list:
    queue, visited = deque(), set()
    queue.append((start, '', []))
    paths = []

    if keypad_name == "directional":
        keypad = __build_directional_keypad()
    else:
        keypad = __build_numerical_keypad()

    while len(queue) != 0:
        current_position = queue.popleft()
        i, j = current_position[0]
        path = current_position[2]

        if current_position[0] == end:
            if len(path) >= 2:
                perms = set(permutations(path, len(path)))
                for p in perms:
                    pp = list(p)
                    if __option_valid(p, start, keypad_name):
                        pp.append('A')
                        paths.append(pp)
            else:
                path.append('A')
                paths.append(path)
            return paths

        neighbors = [(i, j - 1, '<'), (i - 1, j, '^'), (i, j + 1, '>'), (i + 1, j, 'v')]
        for n in neighbors:
            if (n[0], n[1]) in keypad and n not in visited:
                new_path = list(path)
                new_path.append(n[2])
                queue.append(((n[0], n[1]), n[2], new_path))
                visited.add(n)

    raise Exception("No solution found!")


@cache
def get_cost(a, b, keypad_name, depth=0):
    # Cost of going from a to b on given keypad and recursion depth
    if depth == 0:
        return min([len(x) for x in __bfs("directional", a, b)])

    ways = __bfs(keypad_name, a, b)
    options = []
    for o in ways:
        option_str = ""
        for oo in list(o):
            option_str += "".join(oo)
        options.append(option_str)

    best_cost = 1 << 60
    for seq in options:
        seq = "A" + seq
        cost = 0
        for i in range(len(seq) - 1):
            a, b = __find_button_position("directional", seq[i]), __find_button_position("directional", seq[i + 1])
            cost += get_cost(a, b, "directional", depth - 1)
        best_cost = min(best_cost, cost)
    return best_cost


def get_code_cost(code, depth):
    code = "A" + code
    cost = 0
    for i in range(len(code) - 1):
        a, b = __find_button_position("numerical", code[i]), __find_button_position("numerical", code[i + 1])
        cost += get_cost(a, b, "numerical", depth)
    return cost


def __press_keypad(ways, level) -> list:
    if level == 0:
        min_len = sys.maxsize
        for ww in ways:
            min_len = min(min_len, len(ww))
        return min_len

    new_ways = set()
    for w in ways:
        start = (0, 2)
        options = []
        for c in w:
            end = __find_button_position("directional", c)
            options.append(__bfs("directional", start, end))
            start = end
        for o in list(itertools.product(*options)):
            option_str = ""
            for oo in list(o):
                option_str += "".join(oo)
            new_ways.add(option_str)

    return __press_keypad(new_ways, level - 1)

def part_one(data) -> int:

    result = 0
    for code in data.splitlines():
        start = (3, 2)

        ways = []
        for c in code:
            end = __find_button_position("numerical", c)
            ways.append(__bfs( "numerical", start, end))
            start = end

        ways2 = set()
        for o in list(itertools.product(*ways)):
            option_str = ""
            for oo in list(o):
                option_str += "".join(oo)
            ways2.add(option_str)

        result += __press_keypad(ways2, 2) * int(code[0:len(code)-1])
    return result


# William Feng's solution - https://github.com/womogenes/AoC-2024-Solutions/blob/main/day_21/p2_day_21.py
# Explainer video - https://www.youtube.com/watch?v=q5I6ZvJmHEo
def part_two(data) -> int:
    result = 0
    for code in data.splitlines():
        result += get_code_cost(code, 25) * int(code[0:len(code)-1])
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        # print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


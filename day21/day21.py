import itertools
import os.path
import sys
from collections import deque
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


def __find_button_position(keypad, button) -> tuple:
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

def __bfs(keypad, keypad_name, start, end) -> list:
    queue, visited = deque(), set()
    queue.append((start, '', []))
    paths = []

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


def __press_keypad(keypad, keypad_name, code, start, level) -> list:
    if level == 3:
        return code

    new_code = []
    for c in code:
        end = __find_button_position(keypad, c)
        new_code.extend(__bfs(keypad, keypad_name, start, end))
        start = end

    return __press_keypad(__build_directional_keypad(), "directional", new_code, (0, 2), level + 1)

def part_one(data) -> int:
    numerical_keypad = __build_numerical_keypad()
    directional_keypad = __build_directional_keypad()
    result = 0

    for code in data.splitlines():
        start = (3, 2)
        keypad = numerical_keypad
        ways1 = []
        for c in code:
            end = __find_button_position(keypad, c)
            ways1.append(__bfs(keypad, "numerical", start, end))
            start = end

        ways2 = set()
        for o in list(itertools.product(*ways1)):
            option_str = ""
            for oo in list(o):
                option_str += "".join(oo)
            ways2.add(option_str)

        ways3 = set()
        for w in ways2:
            start = (0, 2)
            options = []
            keypad = directional_keypad
            for c in w:
                end = __find_button_position(keypad, c)
                options.append(__bfs(keypad, "directional", start, end))
                start = end
            for o in list(itertools.product(*options)):
                option_str = ""
                for oo in list(o):
                    option_str += "".join(oo)
                ways3.add(option_str)

        ways4 = set()
        for w in ways3:
            start = (0, 2)
            options = []
            keypad = directional_keypad
            for c in w:
                end = __find_button_position(keypad, c)
                options.append(__bfs(keypad, "directional", start, end))
                start = end
            for o in list(itertools.product(*options)):
                option_str = ""
                for oo in list(o):
                    option_str += "".join(oo)
                ways4.add(option_str)

        option_min = sys.maxsize
        for ww in ways4:
            option_min = min(option_min, len(ww) * int(code[0:len(code)-1]))

        result += option_min
    return result

def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


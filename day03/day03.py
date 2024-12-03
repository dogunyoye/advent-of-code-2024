import os.path
import re

DATA = os.path.join(os.path.dirname(__file__), 'day03.txt')


def part_one(data) -> int:
    result = 0
    for m in re.findall(r'mul\((\d+),(\d+)\)', data):
        result += int(m[0]) * int(m[1])
    return result


def part_two(data) -> int:
    result = 0
    enabled = True
    for m in re.findall(r'mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))', data):
        if enabled and m[0].isnumeric():
            result += int(m[0]) * int(m[1])
        elif m[2] == 'do()':
            enabled = True
        elif m[3] == "don't()":
            enabled = False
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

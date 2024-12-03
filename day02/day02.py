import copy
import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day02.txt')


def __is_safe(level) -> bool:
    diffs = []
    for i in range(len(level) - 1):
        diffs.append(level[i] - level[i + 1])

    return all(-3 <= val <= -1 for val in diffs) or all(1 <= val <= 3 for val in diffs)


def __can_be_made_safe(level) -> bool:
    for idx in range(len(level)):
        copied = copy.deepcopy(level)
        del copied[idx]
        if __is_safe(copied):
            return True
    return False


def part_one(data) -> int:
    result = 0
    for line in data.splitlines():
        level = [int(ele) for ele in line.split()]
        if __is_safe(level):
            result += 1
    return result


def part_two(data) -> int:
    result = 0
    for line in data.splitlines():
        level = [int(ele) for ele in line.split()]
        if __is_safe(level) or __can_be_made_safe(level):
            result += 1
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

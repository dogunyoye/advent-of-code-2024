import copy
import os.path
from collections import defaultdict

from pyllist import dllist

DATA = os.path.join(os.path.dirname(__file__), 'day11.txt')


def __blink_naive(numbers):
    to_insert = -1
    skip = False
    original_size = len(numbers)

    for idx, node in enumerate(numbers.iternodes()):
        if skip:
            continue

        if to_insert != -1:
            numbers.insert(to_insert, before=node)
            to_insert = -1

        if node.value == 0:
            node.value = 1
        elif len(str(node.value)) % 2 == 0:
            num_str = str(node.value)
            half = len(num_str) // 2
            left, right = num_str[0:half], num_str[half:]
            node.value = int(left)

            if idx == original_size - 1:
                numbers.insert(int(right), after=node)
                skip = True
            else:
                to_insert = int(right)
        else:
            node.value *= 2024


def __blink_optimised(numbers):
    new_stones = defaultdict(int)
    for k, v in numbers.items():
        if v > 0:
            if k == 0:
                new_stones[0] -= v
                new_stones[1] += v
            elif len(str(k)) % 2 == 0:
                num_str = str(k)
                half = len(num_str) // 2
                left, right = num_str[0:half], num_str[half:]
                new_stones[k] -= v
                new_stones[int(left)] += v
                new_stones[int(right)] += v
            else:
                new_stones[k] -= v
                new_stones[k*2024] += v

    for k, v in new_stones.items():
        numbers[k] += v


def part_one(data) -> int:
    result = 0
    for n in [int(ele) for ele in data.split()]:
        nums = dllist([n])
        for i in range(25):
            __blink_naive(nums)
        result += len(nums)
    return result


def part_two(data) -> int:
    numbers = defaultdict(int)
    for k in [int(ele) for ele in data.split()]:
        numbers[k] = 1

    for i in range(75):
        __blink_optimised(numbers)

    result = 0
    for v in numbers.values():
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

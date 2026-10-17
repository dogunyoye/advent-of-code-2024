import os.path
from collections import defaultdict
from functools import cache

DATA = os.path.join(os.path.dirname(__file__), 'day11.txt')


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
                new_stones[k * 2024] += v

    for k, v in new_stones.items():
        numbers[k] += v


# for research purposes - slightly slower than __blink_optimised
@cache
def __blink_recursive(stone, blink) -> int:
    if blink == 75:
        return 1

    if stone == 0:
        return __blink_recursive(1, blink + 1)

    if len(str(stone)) % 2 == 0:
        num_str = str(stone)
        half = len(num_str) // 2
        left, right = num_str[0:half], num_str[half:]
        return __blink_recursive(int(left), blink + 1) + __blink_recursive(int(right), blink + 1)

    return __blink_recursive(stone * 2024, blink + 1)


def __count_stones(data, blinks) -> int:
    numbers = defaultdict(int)
    for k in [int(ele) for ele in data.split()]:
        numbers[k] = 1

    for _ in range(blinks):
        __blink_optimised(numbers)

    return sum(numbers.values())


def part_one(data) -> int:
    return __count_stones(data, 25)


def part_two(data) -> int:
    return __count_stones(data, 75)


def __part_two_recursive(data) -> int:
    result = 0
    for stone in [int(ele) for ele in data.split()]:
        result += __blink_recursive(stone, 0)
    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

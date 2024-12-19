import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day19.txt')


def __build_towels(data) -> tuple:
    lines = data.splitlines()
    available_towels = set()
    [available_towels.add(t) for t in lines[0].split(", ")]
    return available_towels, lines[2:]


def __find_towel_combos(towel, available_towels, memo, is_part_one) -> int:
    if len(towel) == 0:
        return 1

    if towel in memo:
        return memo[towel]

    result = 0
    for i in range(0, len(towel)):
        t = towel[0:i+1]
        if t in available_towels:
            result += __find_towel_combos(towel[i+1:], available_towels, memo, is_part_one)
            if is_part_one and result == 1:
                return 1

    memo[towel] = result
    return result


def part_one(data) -> int:
    available_towels, towels = __build_towels(data)
    count = 0
    for t in towels:
        if __find_towel_combos(t, available_towels, {}, True):
            count += 1
    return count


def part_two(data) -> int:
    available_towels, towels = __build_towels(data)
    count = 0
    for t in towels:
        count += __find_towel_combos(t, available_towels, {}, False)
    return count


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


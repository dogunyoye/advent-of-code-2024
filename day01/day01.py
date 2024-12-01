import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day01.txt')


def part_one(data) -> int:
    left, right = [], []
    result = 0
    for line in data.splitlines():
        nums = line.split()
        left.append(int(nums[0]))
        right.append(int(nums[1]))

    left.sort()
    right.sort()

    for i in range(len(left)):
        result += abs(left[i] - right[i])

    return result


def part_two(data) -> int:
    left, right = [], []
    result = 0
    for line in data.splitlines():
        nums = line.split()
        left.append(int(nums[0]))
        right.append(int(nums[1]))

    for n in left:
        result += n * right.count(n)

    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

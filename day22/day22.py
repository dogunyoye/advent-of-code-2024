import os.path
import sys
from collections import defaultdict

DATA = os.path.join(os.path.dirname(__file__), 'day22.txt')


def __evolve_secret_number(secret_number) -> int:
    mul64 = secret_number * 64
    secret_number ^= mul64
    secret_number %= 16777216

    div32 = secret_number // 32
    secret_number ^= div32
    secret_number %= 16777216

    mul2048 = secret_number * 2048
    secret_number ^= mul2048
    secret_number %= 16777216

    return secret_number


def __find_max_bananas(secret_numbers, differences) -> int:
    sequences = defaultdict(list)
    for k, v in differences.items():
        changes = defaultdict(int)
        for i in range(1997):
            seq = tuple(v[i:i + 4])
            if changes[seq] == 0:
                changes[seq] = secret_numbers[k][i + 4]
        for kk, vv in changes.items():
            sequences[kk].append(vv)

    max_bananas = -sys.maxsize
    for v in sequences.values():
        max_bananas = max(max_bananas, sum(v))

    return max_bananas


def part_one(data) -> int:
    result = 0
    for line in data.splitlines():
        secret_number = int(line)
        for _ in range(2000):
            secret_number = __evolve_secret_number(secret_number)
        result += secret_number
    return result


def part_two(data) -> int:
    secret_numbers, differences = {}, {}
    for line in data.splitlines():
        secret_number = int(line)
        original_secret_number = secret_number
        nums = [secret_number % 10]
        diffs = []

        for _ in range(2000):
            prev_secret_number = secret_number
            secret_number = __evolve_secret_number(secret_number)
            nums.append(secret_number % 10)
            diffs.append((secret_number % 10) - (prev_secret_number % 10))

        secret_numbers[original_secret_number] = nums
        differences[original_secret_number] = diffs

    return __find_max_bananas(secret_numbers, differences)


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


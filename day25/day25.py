import os.path
from collections import defaultdict

DATA = os.path.join(os.path.dirname(__file__), 'day25.txt')


def __build_locks_and_keys(data) -> tuple:
    lines = data.splitlines()
    locks, keys = [], []

    for i in range(0, len(lines), 8):
        if lines[i] == "#####":
            is_lock = True
            end_idx_offset = 7
        else:
            is_lock = False
            end_idx_offset = 6

        config = defaultdict(int)
        for c in range(5):
            config[c] = 0

        for j in range(i+1, i+end_idx_offset):
            indices = [i for i, ltr in enumerate(lines[j]) if ltr == '#']
            for idx in indices:
                config[idx] += 1

        if is_lock:
            locks.append(tuple(config.values()))
        else:
            keys.append(tuple(config.values()))
    return locks, keys


def part_one(data) -> int:
    locks, keys = __build_locks_and_keys(data)
    result = 0

    for l in locks:
        for k in keys:
            fits = True
            for i in range(5):
                if l[i] + k[i] > 5:
                    fits = False
                    break
            if fits:
                result += 1

    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


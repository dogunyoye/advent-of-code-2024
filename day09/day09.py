import os.path
from collections import deque

DATA = os.path.join(os.path.dirname(__file__), 'day09.txt')


def __print_disk_map(disk_map):
    disk = ""
    for f in disk_map:
        disk += str(f[0])
    print(disk)


def __build_disk_map(data) -> tuple:
    id_num = 0
    free_space_indices = deque()
    disk_map = []
    disk_map_sizes = {}
    rolling_idx = 0

    for idx, c in enumerate(data):
        if idx % 2 == 0:
            f_idx = rolling_idx
            for _ in range(int(c)):
                rolling_idx += 1
                disk_map.append((str(id_num),))
            disk_map_sizes[id_num] = (f_idx, int(c))
            id_num += 1
        else:
            for _ in range(int(c)):
                rolling_idx += 1
                disk_map.append(('.',))

    for idx, c in enumerate(disk_map):
        if c[0] == '.':
            free_space_indices.append(idx)

    return disk_map, free_space_indices, disk_map_sizes


def __has_free_blocks(disk_map, f_idx, f_size) -> tuple:
    free_blocks = 0
    start_idx = 0

    for idx, i in enumerate(range(f_idx)):
        if disk_map[i][0] == '.':
            if free_blocks == 0:
                start_idx = idx
            free_blocks += 1
            if free_blocks == f_size:
                return True, start_idx
        else:
            free_blocks = 0
            start_idx = 0

    return False, -1


def part_one(data) -> int:
    disk_map, free_space_indices, _ = __build_disk_map(data)
    checksum = 0

    for idx, c in enumerate(reversed(disk_map)):
        if len(free_space_indices) == 0 or free_space_indices[0] > len(disk_map) - idx - 1:
            break
        if c[0] != '.':
            disk_map[free_space_indices.popleft()] = (c[0],)
            disk_map[len(disk_map) - idx - 1] = ('.',)

    for idx, c in enumerate(disk_map):
        if c[0] != '.':
            checksum += idx * int(c[0])

    return checksum


def part_two(data) -> int:
    disk_map, _, disk_map_sizes = __build_disk_map(data)
    keys = disk_map_sizes.keys()
    checksum = 0

    for f in reversed(keys):
        f_size = disk_map_sizes[f][1]
        f_idx = disk_map_sizes[f][0]
        has_free, free_idx = __has_free_blocks(disk_map, f_idx, f_size)
        if has_free:
            for i in range(free_idx, free_idx + f_size):
                disk_map[i] = (f,)
            for j in range(f_idx, f_idx + f_size):
                disk_map[j] = ('.',)

    for idx, c in enumerate(disk_map):
        if c[0] != '.':
            checksum += idx * int(c[0])

    return checksum


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

import os.path

DATA = os.path.join(os.path.dirname(__file__), 'day05.txt')


def __build_orderings_maps(data) -> dict:
    ordering = {}
    for line in data.splitlines():
        if line == "":
            break
        parts = line.split("|")
        first, second = int(parts[0]), int(parts[1])
        if first not in ordering:
            ordering[first] = [second]
        else:
            ordering[first].append(second)
    return ordering


def __build_updates_list(data) -> list:
    updates = []
    for line in data.splitlines():
        if "," in line:
            update = [int(x) for x in line.split(',')]
            updates.append(update)
    return updates


def part_one(data) -> int:
    orderings = __build_orderings_maps(data)
    updates = __build_updates_list(data)
    result = 0

    for u in updates:
        valid = True
        for idx, n in enumerate(u[1:]):
            if n not in orderings:
                continue
            for i in range(idx+1):
                if u[i] in orderings[n]:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            result += u[len(u)//2]

    return result


def part_two(data) -> int:
    orderings = __build_orderings_maps(data)
    updates = __build_updates_list(data)
    result = 0
    invalid_updates = []

    for u in updates:
        valid = True
        for idx, n in enumerate(u[1:]):
            if n not in orderings:
                continue
            for i in range(idx+1):
                if u[i] in orderings[n]:
                    valid = False
                    invalid_updates.append(u)
                    break
            if not valid:
                break

    for iu in invalid_updates:
        valid = False
        while not valid:
            valid = True
            for idx, n in enumerate(iu[1:]):
                if n not in orderings:
                    continue
                for i in range(idx + 1):
                    if iu[i] in orderings[n]:
                        swap_idx = iu.index(n)
                        iu[i], iu[swap_idx] = iu[swap_idx], iu[i]
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                result += iu[len(iu)//2]

    return result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

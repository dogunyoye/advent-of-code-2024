import os.path
from itertools import product

DATA = os.path.join(os.path.dirname(__file__), 'day07.txt')

completed = set()
part1 = 0


def part_one(data) -> int:
    result = 0
    for idx, line in enumerate(data.splitlines()):
        line = line.replace(":", "")
        nums = [int(ele) for ele in line.split()]
        test_val = nums[0]
        n = len(nums) - 1
        for p in product(['*', '+'], repeat=n - 1):
            equation = ""
            for i in range(1, len(nums)):
                equation += str(nums[i])
                if '+' in equation:
                    parts = equation.split("+")
                    equation = str(int(parts[0]) + int(parts[1]))
                elif '*' in equation:
                    parts = equation.split("*")
                    equation = str(int(parts[0]) * int(parts[1]))
                if i <= len(p):
                    equation += p[i - 1]

            if int(equation) == test_val:
                result += test_val
                global completed
                completed.add(idx)
                break

    global part1
    part1 = result

    return result


# Note: Python's eval() is much slower than simply using
# natural operators. Hence, part two just uses the latter
def part_two(data) -> int:
    result = 0
    prods_cache = {}

    for idx, line in enumerate(data.splitlines()):
        if idx in completed:
            continue
        line = line.replace(":", "")
        nums = [int(ele) for ele in line.split()]
        test_val = nums[0]
        n = len(nums) - 1

        if (n - 1) not in prods_cache:
            prods_cache[(n - 1)] = list(product(['*', '+', '||'], repeat=n - 1))
            prods = prods_cache[(n - 1)]
        else:
            prods = prods_cache[(n - 1)]

        for p in prods:
            equation = ""
            if '||' not in p:
                continue

            for i in range(1, len(nums)):
                equation += str(nums[i])
                if '+' in equation:
                    parts = equation.split("+")
                    equation = str(int(parts[0]) + int(parts[1]))
                elif '*' in equation:
                    parts = equation.split("*")
                    equation = str(int(parts[0]) * int(parts[1]))
                elif '||' in equation:
                    parts = equation.split("||")
                    equation = parts[0] + parts[1]

                if equation.isnumeric() and int(equation) > test_val:
                    break

                if i <= len(p):
                    equation += p[i - 1]

            if int(equation) == test_val:
                result += test_val
                break

    return part1 + result


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

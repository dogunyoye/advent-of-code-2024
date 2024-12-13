import os.path
import sympy as sym
import re

from sympy import Integer

DATA = os.path.join(os.path.dirname(__file__), 'day13.txt')


def __build_claw_machine_settings(data) -> dict:
    claw_machine_settings = {}
    lines = data.splitlines()
    machine_id = 0

    for i in range(0, len(lines), 4):
        (xa, ya) = re.findall(r'Button A: X\+(\d+), Y\+(\d+)', lines[i])[0]
        (xb, yb) = re.findall(r'Button B: X\+(\d+), Y\+(\d+)', lines[i + 1])[0]
        (prize_x, prize_y) = re.findall(r'Prize: X=(\d+), Y=(\d+)', lines[i + 2])[0]
        claw_machine_settings[machine_id] = [(int(xa), int(ya)), (int(xb), int(yb)), (int(prize_x), int(prize_y))]
        machine_id += 1

    return claw_machine_settings


# research purposes - using sympy to solve the simultaneous equation
# VERY SLOW (~7s)
# https://reliability.readthedocs.io/en/latest/Solving%20simultaneous%20equations%20with%20sympy.html
def __find_claw_machine_cost_sympy(settings) -> int:
    (xa, ya) = settings[0]
    (xb, yb) = settings[1]
    (prize_x, prize_y) = settings[2]

    x, y = sym.symbols('x,y')
    eq1 = sym.Eq(xa * x + xb * y, prize_x)
    eq2 = sym.Eq(ya * x + yb * y, prize_y)
    result = sym.solve([eq1, eq2], (x, y))

    x_val, y_val = result[x], result[y]
    if isinstance(x_val, Integer) and isinstance(y_val, Integer):
        return (3 * x_val) + y_val

    # no solution
    return 0


# https://en.wikipedia.org/wiki/Cramer%27s_rule#Explicit_formulas_for_small_systems
def __find_claw_machine_cost(settings) -> int:
    (xa, ya) = settings[0]
    (xb, yb) = settings[1]
    (prize_x, prize_y) = settings[2]

    a = ((prize_x * yb) - (prize_y * xb)) // ((xa * yb) - (ya * xb))
    b = ((xa * prize_y) - (ya * prize_x)) // ((xa * yb) - (ya * xb))

    if ((a * xa) + (b * xb)) == prize_x:
        return (3 * a) + b

    # no solution
    return 0


def part_one(data) -> int:
    claw_settings_machines = __build_claw_machine_settings(data)
    tokens = 0
    for k, v in claw_settings_machines.items():
        tokens += __find_claw_machine_cost(v)
    return tokens


def part_two(data) -> int:
    claw_settings_machines = __build_claw_machine_settings(data)
    tokens = 0
    for k, v in claw_settings_machines.items():
        (prize_x, prize_y) = v[2]
        v[2] = (prize_x + 10000000000000, prize_y + 10000000000000)
        tokens += __find_claw_machine_cost(v)
    return tokens


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

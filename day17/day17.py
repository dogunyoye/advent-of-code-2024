import os.path
import re
from collections import deque


DATA = os.path.join(os.path.dirname(__file__), 'day17.txt')


class Computer(object):

    def __init__(self, registers, program):
        self.registers = registers
        self.program = program
        self.instruction_pointer = 0
        self.out = []
        self.functions = {
            0: ('C', self.__adv),
            1: ('L', self.__bxl),
            2: ('C', self.__bst),
            3: ('L', self.__jnz),
            4: ('I', self.__bxc),
            5: ('C', self.__out),
            6: ('C', self.__bdv),
            7: ('C', self.__cdv)
        }

    def __adv(self, operand):
        self.registers['A'] //= (2 ** operand)

    def __bxl(self, operand):
        self.registers['B'] ^= operand

    def __bst(self, operand):
        self.registers['B'] = operand % 8

    def __jnz(self, operand):
        if self.registers['A'] == 0:
            self.instruction_pointer += 2
            return

        self.instruction_pointer = operand

    def __bxc(self, _operand):
        self.registers['B'] ^= self.registers['C']

    def __out(self, operand):
        self.out.append(operand % 8)

    def __bdv(self, operand):
        self.registers['B'] = self.registers['A'] // (2 ** operand)

    def __cdv(self, operand):
        self.registers['C'] = self.registers['A'] // (2 ** operand)

    def execute_program(self):
        while 0 <= self.instruction_pointer < len(self.program):
            opcode = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer+1]

            if self.functions[opcode][0] == 'C':
                if operand == 4:
                    operand = self.registers['A']
                elif operand == 5:
                    operand = self.registers['B']
                elif operand == 6:
                    operand = self.registers['C']

            self.functions[opcode][1](operand)
            if opcode == 3:
                continue

            self.instruction_pointer += 2

    # disassembled function specific to my input
    # likely faster than parsing each instruction
    def execute_program_disassembled(self):
        a = self.registers['A']

        while a != 0:
            b = a % 8
            b = b ^ 5
            c = a // (2 ** b) # (1 << b)
            b = b ^ c
            b = b ^ 6
            a = a // (2 ** 3) # (1 << 3)
            self.out.append(b % 8)


    def output(self) -> str:
      return str(self.out).replace("[", "").replace("]", "").replace(" ", "")


def __initialise_registers_and_program(data) -> tuple:
    lines = data.splitlines()
    registers = {}

    for i in range(3):
        (register_id, value) = re.findall(r'Register ([ABC]): (\d+)', lines[i])[0]
        registers[register_id] = int(value)

    program = [int(x) for x in lines[len(lines) - 1].split(": ")[1].split(',')]
    return registers, program


def part_one(data) -> str:
    registers, program = __initialise_registers_and_program(data)
    c = Computer(registers, program)
    c.execute_program_disassembled()
    return c.output()


def part_two(data) -> int:
    registers, program = __initialise_registers_and_program(data)
    program_str = str(program).replace("[", "").replace("]", "").replace(" ", "")
    program_str = program_str.replace(",", "")

    candidates = deque()
    candidates.append((0, 0))

    while len(candidates) != 0:
        (candidate, length) = candidates.popleft()
        if length == len(program):
            return candidate

        to_find = program_str[len(program_str) - 1 - length:]
        for i in range(candidate*8, candidate*8 + 8):
            c = Computer({"A": i, "B": 0, "C": 0}, program)
            c.execute_program_disassembled()
            expected = c.output().replace(",", "")
            if expected.endswith(to_find):
                candidates.append((i, length + 1))

    raise Exception("No solution found!")


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + part_one(data))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


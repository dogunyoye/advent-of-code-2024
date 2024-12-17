import os.path
import re

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

    def __bxc(self, operand):
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

def __binary_convert(output) -> str:
    result = ""
    for num in output.split(","):
        result += bin(int(num))[2:]
    return result

def part_one(data) -> str:
    registers, program = __initialise_registers_and_program(data)
    c = Computer(registers, program)
    c.execute_program()
    return c.output()

def part_two(data) -> int:
    registers, program = __initialise_registers_and_program(data)
    program_str = str(program).replace("[", "").replace("]", "").replace(" ", "")
    value = 0

    # for every base 8 number we set register A to
    # the number of output values increases.
    # There are 16 numbers in my input program
    # => 8^15 = 35184372088832

    start = -1

    while True:
        registers = {"A": 8 ** value, "B": 0, "C": 0}
        c = Computer(registers, program)
        c.execute_program()
        if len(c.output().split(",")) == 16:
            start = 8 ** value
            break
        value += 1

    while True:
        registers = {"A": start, "B": 0, "C": 0}
        c = Computer(registers, program)
        c.execute_program()
        print(start)
        print(bin(start)[2:])
        print(c.output())
        print(__binary_convert(c.output()))
        print()
        if c.output() == program_str:
            return start
        start += 1


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + part_one(data))
        print("Part 2: " + str(part_two(data)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())


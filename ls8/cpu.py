"""CPU functionality."""

import sys

MUL = 0b10100010
ADD = 0b10100000
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
PSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        path = sys.argv[1]

        file = open(path)
        program_file = file.readlines()
        program = []
        for line in program_file:
            if line[0] == '#' or line[0] == '\n':
                pass
            else:
                program.append(int(line[:8], 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(loc):
        return self.ram[loc]

    def ram_write(loc, val):
        self.ram[loc] = val

    def run(self):
        """Run the CPU."""
        pc = self.pc
        SP = 0xF3

        while True:
            IR = self.ram[pc]
            if IR == HLT:
                break
            elif IR == LDI:
                opa = self.ram[pc + 1]
                opb = self.ram[pc + 2]
                pc += 3
                self.reg[opa] = opb

            elif IR == PRN:
                reg_loc = self.ram[pc + 1]
                print(self.reg[reg_loc])
                pc += 2

            elif IR == ADD:
                opa = self.ram[pc + 1]
                opb = self.ram[pc + 2]
                self.alu('ADD', opa, opb)
                pc += 3

            elif IR == MUL:
                opa = self.ram[pc + 1]
                opb = self.ram[pc + 2]
                self.alu('MUL', opa, opb)
                pc += 3

            elif IR == PSH:
                opa = self.ram[pc + 1]
                self.ram[SP] = self.reg[opa]
                SP -= 1
                pc += 2


            elif IR == POP:
                opa = self.ram[pc + 1]
                SP += 1
                self.reg[opa] = self.ram[SP]
                pc += 2




cpu = CPU()
cpu.load()
cpu.run()

import sys
from enum import Enum


class CommandType(Enum):
    A = 1
    C = 2
    L = 3


class Parser():
    """Parser parse each line into parts depend on commandType"""
    def __init__(self, file_name):
        self._file_name = file_name
        self._file = open(file_name, "r")

    def advance(self):
        self._current_line = self._file.readline()
        self._current_command = self._current_line[:self._current_line.
                                                   find(r"//")].strip()
        if self._current_command == "\n" or self._current_command == "":
            if self.hasMoreCommands():
                self.advance()
        p1 = self._current_command.find("=")
        p2 = self._current_command.find(";")
        if p2 == -1: p2 = len(self._current_command)

        self._dest = self._current_command[:p1] if p1 != -1 else ""
        self._comp = self._current_command[p1 + 1:p2]
        self._jump = self._current_command[p2 + 1:]

    def hasMoreCommands(self):
        return self._current_line != ""

    def commandType(self):
        if self._current_command[0] == "(":
            return CommandType.L
        if self._current_command[0] == "@":
            return CommandType.A
        return CommandType.C

    def symbol(self):
        if self.commandType() == CommandType.A:
            return self._current_command[1:]
        return self._current_command[1:-1]

    def dest(self):
        return self._dest

    def comp(self):
        return self._comp

    def jump(self):
        return self._jump


class Code():
    """Translates Hack assembly language mnemonics into binary codes."""
    @staticmethod
    def dest(dd):
        d1 = "1" if "A" in dd else "0"
        d2 = "1" if "D" in dd else "0"
        d3 = "1" if "M" in dd else "0"
        return d1 + d2 + d3

    @staticmethod
    def comp(cc):
        a = "1" if "M" in cc else "0"
        cc = cc.replace("M", "A")
        if cc == "0":
            c = "101010"
        if cc == "1":
            c = "111111"
        if cc == "-1":
            c = "111010"
        if cc == "D":
            c = "001100"
        if cc == "A":
            c = "110000"
        if cc == "!D":
            c = "001101"
        if cc == "!A":
            c = "110001"
        if cc == "-D":
            c = "001111"
        if cc == "-A":
            c = "110011"
        if cc == "D+1":
            c = "011111"
        if cc == "A+1":
            c = "110111"
        if cc == "D-1":
            c = "001110"
        if cc == "A-1":
            c = "110010"
        if cc == "D+A":
            c = "000010"
        if cc == "D-A":
            c = "010011"
        if cc == "A-D":
            c = "000111"
        if cc == "D&A":
            c = "000000"
        if cc == "D|A":
            c = "010101"
        return a + c

    @staticmethod
    def jump(jj):
        if jj == "JGT": return "001"
        if jj == "JEQ": return "010"
        if jj == "JGE": return "011"
        if jj == "JLT": return "100"
        if jj == "JNE": return "101"
        if jj == "JLE": return "110"
        if jj == "JMP": return "111"
        return "000"

    @staticmethod
    def decimalToBinary(num):
        rs = ""
        count = 0
        while count < 15:
            rs = str(num % 2) + rs
            num //= 2
            count += 1
        return rs


class SymbolTable():
    """Keeps a correspondence between symbolic lables and numeric address"""
    def __init__(self):
        self._table = dict()
        table = self._table
        # define predefine symbol
        table["SP"] = 0
        table["LCL"] = 1
        table["ARG"] = 2
        table["THIS"] = 3
        table["THAT"] = 4
        table["SCREEN"] = 16384
        table["KBD"] = 24576
        for i in range(16):
            table["R" + str(i)] = i
        self._free_address = 16

    def addEntr(self, symbol, address):
        self._table[symbol] = address

    def contains(self, symbol):
        return symbol in self._table

    def get_address(self, symbol):
        return self._table[symbol]

    def get_free_address(self):
        self._free_address += 1
        return self._free_address - 1


if __name__ == "__main__":
    in_filename = sys.argv[1]
    out_filename = in_filename.split(".")[0] + ".hack"
    # Initialize symbol table
    t = SymbolTable()

    # First pass: add all labels
    p1 = Parser(in_filename)
    p1.advance()
    counter = 0
    while p1.hasMoreCommands():
        if p1.commandType() == CommandType.L:
            label = p1.symbol()
            t.addEntr(label, counter)
        else:
            counter += 1
        p1.advance()

    # Second pass
    p2 = Parser(in_filename)
    f = open(out_filename, "w")
    p2.advance()
    while p2.hasMoreCommands():
        binaryCode = str()
        num = int()
        if p2.commandType() == CommandType.A:
            symbol = p2.symbol()
            try:
                num = int(symbol)
            except ValueError:
                if not t.contains(symbol):
                    t.addEntr(symbol, t.get_free_address())
                num = t.get_address(symbol)
            binaryCode = "0" + Code.decimalToBinary(num)
        elif p2.commandType() == CommandType.C:
            binaryCode = "111" + Code.comp(p2.comp()) + Code.dest(
                p2.dest()) + Code.jump(p2.jump())
        else:
            p2.advance()
            continue
        print(p2._current_command, "\t", binaryCode)
        f.write(binaryCode + "\n")
        p2.advance()

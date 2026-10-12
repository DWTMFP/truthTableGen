import argparse

import matplotlib as mpl
import matplotlib.pyplot as plt

# change font of LaTeXs
mpl.rc("text", usetex=False)
mpl.rc("font", family="serif")
mpl.rc("mathtext", fontset="cm")

type TruthTable = list[list[str]]


def boolToStr(b: bool) -> str:
    return "w" if b else "f"


def getStatements() -> list[str]:
    return ["A", "B", "C"]


def addTruthValues(truthTable: TruthTable, cycle_len: int, num_rows: int) -> None:
    row = 1
    truthValue = True
    for column in range(len(truthTable)):
        while row < num_rows:
            for _ in range(cycle_len):
                truthTable[row].append(boolToStr(truthValue))
                row += 1
            truthValue = not truthValue


def createEmtpyTable(statements: list[str]) -> TruthTable:
    num_rows = 2 ** len(statements) + 1  # +1 for accounting "description"

    # for accessing with truthTable[row], otherwise an append would be necessary
    truthTable: TruthTable = [[] for i in range(num_rows)]
    for cycle_exp, statement in enumerate(statements):
        truthTable[0].append(statement)
        # Starting with the biggest exponent
        cycle_len = 2 ** (len(statements) - cycle_exp - 1)
        addTruthValues(truthTable, cycle_len, num_rows)
    return truthTable


def createTexString(truthTable: TruthTable) -> str:
    tex_str = "\\begin{table}\n\\label{}\n\\caption{}\n"
    tex_str += "\\begin{tabular}{" + "c" * len(truthTable[0]) + "}\n"
    for line in truthTable:
        tex_str += " & ".join(line).removeprefix(" & ") + " \\\\ \n"
    tex_str += "\\end{tabular}\n\\end{table}"
    return tex_str


def displayTableInTerminal(truthTable) -> None:
    # Add first row here to avoid if else in for loop
    s = " " + " | ".join(truthTable[0])
    print(s, end="\n" + "-" * (len(s) + 1) + "\n")

    # Start from 1, to not include first row
    for row in range(1, len(truthTable)):
        print(" " + " | ".join(truthTable[row]))


def main() -> None:
    truthTable = createEmtpyTable(getStatements())
    # createTexString(truthTable)
    displayTableInTerminal(truthTable)


if __name__ == "__main__":
    main()

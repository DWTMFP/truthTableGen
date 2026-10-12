import matplotlib as mpl

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
    truthTable: truthTable = [
        [] for i in range(num_rows)
    ]  # for accessing with truthTable[row], otherwise an append would be necessary
    for cycle_exp, statement in enumerate(statements):
        truthTable[0].append(statement)
        cycle_len = (
            2 ** (len(statements) - cycle_exp - 1)
        )  # Starting with the biggest exponent        addTruthValues(truthTable, cycle_len, num_rows)
        addTruthValues(truthTable, cycle_len, num_rows)
    return truthTable


def main() -> None:
    print(*createEmtpyTable(getStatements()), sep="\n")


if __name__ == "__main__":
    main()

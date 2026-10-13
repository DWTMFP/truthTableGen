import argparse
import itertools
import logging
import re
from collections.abc import Sequence
from enum import StrEnum
from pathlib import Path

import yaml

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger()

type TruthTable = list[list[str]]

OPERANDS = frozenset({"v", "^", "xor", "!", "<=>", "=>"})
SUPPORTED_OPERANDS = frozenset({})

# Operands:
# land: A and B
# lor: A or B
# lxor: A ^ B
# equiv(<=>) : not(A ^ B)
# Implikation: not A or B


class gridTypes(StrEnum):
    all = "all"
    partial = "partial"
    none = "None"


SUPPORTED_GRIDS = frozenset({gridTypes.all, gridTypes.partial, gridTypes.none})


class ConfigError(Exception):
    "Error when config doesn't match expectations"

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def getConfig() -> dict[str:str]:
    config_file = Path(__file__).parent / "config.yaml"
    data = yaml.safe_load(config_file.read_text())

    if "grid" not in data:
        raise ConfigError(
            "Du Penner hast grid abgeändert. In der Config muss grid: stehen!"
            f" Du hast {' '.join(data.keys())}"
        )
    if not data["grid"] in SUPPORTED_GRIDS:
        raise ConfigError(
            '"grid" MUSS entweder "all", "partial" oder "None" sein.'
            f" Du hast: {data['grid']}"
        )
    return data


def get_variables(formulas: list[str]) -> list[str]:
    """Erkennt Variablen wie A, B und C in der Formel."""
    variables = set()

    for formula in formulas:
        variables.update(re.findall(r"\b[A-Z]\b", formula))

    if not variables:
        raise ValueError("Keine Variablen gefunden.")

    return sorted(variables)


def generate_rows(variables) -> TruthTable:
    """Generates only the rows for truth values. E.g. [["w","w"], ["w","f"],...]"""
    return list(itertools.product(["w", "f"], repeat=len(variables)))


def display_terminal_table(truthTable: TruthTable, grid: str) -> None:
    """
    Prints the truth table in the terminal.

    :param TruthTable truthTable: The truth table containing all its contents.
    :param Config.grid grid: The grid setting from the configuration file.
    """

    for i in range(len(truthTable)):
        truthTable[i][0] = " " + truthTable[i][0]

    # list[width(column), width(column1), ...]
    widths = [
        max(len(str(row[i])) for row in truthTable) for i in range(len(truthTable[0]))
    ]

    def format_row(row):
        if grid == gridTypes.all:
            return (
                "│"
                + " │ ".join(
                    str(value).center(widths[i]) for i, value in enumerate(row)
                )
                + "│"
            )

        elif grid == gridTypes.partial:
            # Centered " A | B ..."
            return " │ ".join(
                str(value).center(widths[i]) for i, value in enumerate(row)
            )
        # Centerd " A   B   ..."
        return "   ".join(str(value).center(widths[i]) for i, value in enumerate(row))

    # The + "--" is for acounting the "|"
    top_rule = "┌" + "─┬─".join("─" * w for w in widths) + "┐"
    bottom_rule = "└" + "─┴─".join("─" * w for w in widths) + "┘"

    hline = "─┼─".join("─" * w for w in widths)
    if grid == gridTypes.all:
        hline = "├" + hline + "┤"

    if grid == gridTypes.all:
        print(top_rule)
    print(format_row(truthTable[0]))
    if grid != gridTypes.none:
        print(hline)

    for i in range(1, len(truthTable)):
        print(format_row(truthTable[i]))
        if grid == gridTypes.all and i != len(truthTable) - 1:
            print(hline)

    if grid == gridTypes.all:
        print(bottom_rule)


def createTexString(truthTable: TruthTable, grid: str) -> str:
    latexGrid = "c" * len(truthTable[0])
    if grid == gridTypes.all:
        latexGrid = "|" + "c|" * len(truthTable[0])
    elif grid == gridTypes.partial:
        latexGrid = ("c|" * len(truthTable[0])).removesuffix("|")

    def editLine(row: str, curr_row: int):
        if curr_row == 0 and grid != gridTypes.none:
            return row + "\\hline \\\\ \n"
        if grid == gridTypes.all:
            return row + "\\hline \\\\ \n"
        return row + "\\\\ \n"

    tex_str = "\\begin{table}\n\\label{}\n\\caption{}\n"
    tex_str += "\\begin{tabular}{" + latexGrid + "}\n"
    for curr_row, line in enumerate(truthTable):
        tex_str += editLine(" & ".join(line).removeprefix(" & "), curr_row)
    tex_str += "\\end{tabular}\n\\end{table}"
    return tex_str


def getTruthValue(variable: str, truthTable: TruthTable, row: int) -> str:
    pass


def getCompleteTruthTable() -> TruthTable:
    incomplete_table = getTruthTable()

    return []


def getTruthTable(formulas: list[str]) -> TruthTable:
    formulas = [format_operator(f) for f in formulas]
    variables = get_variables(formulas)

    # TODO: Implement subformular detection

    # e.g. headers = ["A", "B", ..., "AvB", ..., "(AvB)vC", ...]
    headers = variables + formulas
    # e.g. rows = [["w","w","w","",""], ["w","w","f","",""], ...]
    rows: TruthTable = [
        list(values) + [""] * len(formulas) for values in generate_rows(variables)
    ]
    # e.g. [["A", "B", "C", "AvB", "BvC"], ["w","w","w","",""], ["w","w","f","",""], ...]
    return [headers] + rows


def format_operator(text, operators=("v",)):
    pattern = r"\s*(" + "|".join(map(re.escape, operators)) + r")\s*"
    return re.sub(pattern, r" \1 ", text).strip()


def main(args: Sequence[str] | None = None):
    if args.formulas is None:
        parser.error("Keine Formeln gefunden")

    try:
        config = getConfig()
    except ConfigError as e:
        logger.warning(str(e))
        logger.info("Now using default Values.")
        config = {"grid": gridTypes.all}

    truthTable = getTruthTable(args.formulas)

    if args.tex:
        print(createTexString(truthTable, config["grid"]))

    if not (args.tex and args.noCLI):
        display_terminal_table(truthTable, config["grid"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator für Wahrheitstabellen")

    parser.add_argument("formulas", nargs="+", help="Logische Formeln, z. B. AvB BvA")

    parser.add_argument(
        "--tex",
        action="store_true",
        help="LaTeX-Code zusätzlich zu der Terminaltabelle ausgeben",
    )

    parser.add_argument(
        "--noCLI",
        action="store_true",
        help="Wahrheitstabelle nicht in Kommandozeile anzeigen",
    )

    main(parser.parse_args())

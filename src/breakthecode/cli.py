from argparse import ArgumentParser, ArgumentTypeError
from typing import List

from rich import print

from breakthecode.constraints import ColorConstraint, OddEvenConstraint, PositionConstraint, SumConstraint
from breakthecode.model import ALL_NUMBERS, Color, Number, SolutionsManager


def number_builder(arg: str) -> Number:
    if len(arg) not in [1, 2]:
        raise ArgumentTypeError("Invalid length for number: " + arg)
    if arg[0] > "9" or arg[0] < "0":
        raise ArgumentTypeError("Number first character is not a digit: " + arg)
    digit = int(arg[0])
    color = None
    if digit == 5:
        color = Color.GREEN
    elif len(arg) == 2:
        if arg[1].lower() == "w":
            color = Color.WHITE
        elif arg[1].lower() == "b":
            color = Color.BLACK
    if color is None:
        raise ArgumentTypeError("Invalid color for number: " + arg)
    candidate = Number(digit, color)
    if candidate not in ALL_NUMBERS:
        raise ArgumentTypeError("Unknown number: " + arg)
    return candidate


def sum_constraint_builder(arg: str) -> SumConstraint:
    digits = []
    for part in arg.split(","):
        try:
            digits.append(int(part))
        except ValueError:
            raise ArgumentTypeError("Invalid number: " + part)
    if len(digits) == 0 or len(digits) > 3:
        raise ArgumentTypeError("Invalid sum spec: " + arg)
    return SumConstraint(digits[0], digits[1] if len(digits) > 1 else 0, digits[2] if len(digits) > 2 else None)


def pos_constraint_builder(arg: str) -> PositionConstraint:
    parts = arg.split(",")
    if len(parts) != 2:
        raise ArgumentTypeError("Invalid pos spec: " + arg)
    number = number_builder(parts[0])
    try:
        pos = int(parts[1])
        return PositionConstraint(number, pos)
    except ValueError:
        raise ArgumentTypeError("Invalid position: " + parts[1])


class HelperCli:
    def __init__(self, argv: List[str]):
        # Build parser
        self.parser = ArgumentParser(description="BreakTheCode board game helper")

        # Removed digits
        self.parser.add_argument(
            "--remove",
            "-r",
            metavar="DC",
            dest="removed_ones",
            action="append",
            type=number_builder,
            default=[],
            help="number that can't be part of the solution (e.g. 0b, 6w, 5)",
        )

        # Sum constraints
        self.parser.add_argument(
            "--sum",
            "-s",
            metavar="T[,I[,C]]",
            dest="sum_constraints",
            action="append",
            type=sum_constraint_builder,
            default=[],
            help="add a sum constraint (T=total, I=start, C=count)",
        )

        # Digit by position constraint
        self.parser.add_argument(
            "--position",
            "-p",
            metavar="N,I",
            dest="pos_constraints",
            action="append",
            type=pos_constraint_builder,
            default=[],
            help="add a position constraint (N=number, I=position)",
        )

        # Odd constraint
        self.parser.add_argument(
            "--odd",
            "-o",
            metavar="O",
            dest="odd_constraint",
            type=lambda c: OddEvenConstraint(True, int(c)),
            default=None,
            help="add an odd numbers count constraint",
        )

        # Even constraint
        self.parser.add_argument(
            "--even",
            "-e",
            metavar="E",
            dest="even_constraint",
            type=lambda c: OddEvenConstraint(False, int(c)),
            default=None,
            help="add an even numbers count constraint",
        )

        # Black constraint
        self.parser.add_argument(
            "--black",
            "-b",
            metavar="B",
            dest="black_constraint",
            type=lambda c: ColorConstraint(Color.BLACK, int(c)),
            default=None,
            help="add a black numbers count constraint",
        )

        # White constraint
        self.parser.add_argument(
            "--white",
            "-w",
            metavar="W",
            dest="white_constraint",
            type=lambda c: ColorConstraint(Color.WHITE, int(c)),
            default=None,
            help="add a white numbers count constraint",
        )

        # Parse args
        self.args = self.parser.parse_args(argv)

    def run(self) -> int:
        # Prepare solution
        m = SolutionsManager(self.args.removed_ones)

        # Summarize constraints
        constraints = list(
            filter(
                lambda c: c is not None,
                (
                    self.args.sum_constraints
                    + self.args.pos_constraints
                    + [self.args.odd_constraint, self.args.even_constraint, self.args.black_constraint, self.args.white_constraint]
                ),
            )
        )
        print("Work with constraints: ", constraints)

        # Compute!
        s = m.compute(constraints)

        # Print them
        print("\nFound solutions candidates:\n" + "\n".join(map(str, s)) + f"\n\nSolution candidates count: {len(s)}")

        return 0 if len(s) == 1 else 1

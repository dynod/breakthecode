from breakthecode.model import Color, Constraint, Number, Solution


# Sum constraint
class SumConstraint(Constraint):
    def __init__(self, expected_sum: int, start_index: int = 0, digits_count: int = None, color_filter: Color = None):
        self.expected_sum = expected_sum
        self.start_index = start_index
        self.digits_count = digits_count
        self.color_filter = color_filter

    def __repr__(self) -> str:
        return f"SumConstraint{self.expected_sum, self.start_index, self.digits_count, self.color_filter}"

    def verify(self, solution: Solution) -> bool:
        return (
            sum(
                n.digit
                for n in filter(
                    lambda n: (self.color_filter is None) or (self.color_filter == n.color),
                    solution.numbers[self.start_index : self.start_index + ((len(solution.numbers) + 1) if self.digits_count is None else self.digits_count)],
                )
            )
            == self.expected_sum
        )


# Constraint for third digit (greater than 4 or net)
class Digit3Constraint(Constraint):
    def __init__(self, greater: bool):
        self.greater = greater

    def verify(self, solution: Solution) -> bool:
        if self.greater:
            return solution.numbers[2].digit > 4
        else:
            return solution.numbers[2].digit <= 4


# Positional constraint
class PositionConstraint(Constraint):
    def __init__(self, number: Number, position: int):
        self.number = number
        self.position = position

    def __repr__(self) -> str:
        return f"PositionConstraint{str(self.number), self.position}"

    def verify(self, solution: Solution) -> bool:
        return solution.numbers[self.position] == self.number


# Odd or even constraint
class OddEvenConstraint(Constraint):
    def __init__(self, odd: bool, count: int):
        self.odd = odd
        self.count = count

    def __repr__(self) -> str:
        return f"OddEvenConstraint{self.odd, self.count}"

    def parity_ok(self, number: Number) -> bool:
        return number.digit % 2 == (1 if self.odd else 0)

    def verify(self, solution: Solution) -> bool:
        return self.count == len(list(filter(self.parity_ok, solution.numbers)))


# Color constraint
class ColorConstraint(Constraint):
    def __init__(self, color: Color, count: int):
        self.color = color
        self.count = count

    def __repr__(self) -> str:
        return f"ColorConstraint{self.color, self.count}"

    def verify(self, solution: Solution) -> bool:
        return len(list(filter(lambda n: n.color == self.color, solution.numbers))) == self.count


# Max-min diff constraint
class DiffConstraint(Constraint):
    def __init__(self, diff: int):
        self.diff = diff

    def __repr__(self) -> str:
        return f"DiffConstraint({self.diff})"

    def verify(self, solution: Solution) -> bool:
        return (solution.numbers[-1].digit - solution.numbers[0].digit) == self.diff

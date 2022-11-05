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


# Constraint for digit
class DigitConstraint(Constraint):
    def __init__(self, greater: bool, index: int = 2, value: int = 4):
        self.greater = greater
        self.index = index
        self.value = value

    def __repr__(self) -> str:
        return f"DigitConstraint{self.greater, self.index, self.value}"

    def verify(self, solution: Solution) -> bool:

        return (solution.numbers[self.index].digit > self.value) if self.greater else (solution.numbers[self.index].digit <= self.value)


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


# Constraint for digit pairs
class PairsConstraint(Constraint):
    def __init__(self, count: int):
        self.count = count

    def __repr__(self) -> str:
        return f"PairsConstraint{self.count}"

    def verify(self, solution: Solution) -> bool:
        pairs_count = 0
        for i in range(len(solution.numbers) - 1):
            if solution.numbers[i].digit == solution.numbers[i + 1].digit:
                pairs_count += 1
        return pairs_count == self.count

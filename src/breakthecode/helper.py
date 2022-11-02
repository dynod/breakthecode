from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List


# Color enum
class Color(Enum):
    BLACK = 0
    WHITE = 1
    GREEN = 2


# Class representing candidate number
@dataclass
class Number:
    digit: int
    color: Color


# All candidate numbers
ALL_NUMBERS = [
    Number(0, Color.BLACK),
    Number(0, Color.WHITE),
    Number(1, Color.BLACK),
    Number(1, Color.WHITE),
    Number(2, Color.BLACK),
    Number(2, Color.WHITE),
    Number(3, Color.BLACK),
    Number(3, Color.WHITE),
    Number(4, Color.BLACK),
    Number(4, Color.WHITE),
    Number(5, Color.GREEN),
    Number(5, Color.GREEN),
    Number(6, Color.BLACK),
    Number(6, Color.WHITE),
    Number(7, Color.BLACK),
    Number(7, Color.WHITE),
    Number(8, Color.BLACK),
    Number(8, Color.WHITE),
    Number(9, Color.BLACK),
    Number(9, Color.WHITE),
]


# Candidate solution
@dataclass
class Solution:
    numbers: List[Number] = field(default_factory=list)

    @property
    def total_sum(self) -> int:
        # Sum for this solution
        return sum(n.digit for n in self.numbers)


# Constraint for solution
class Constraint(ABC):
    @abstractmethod
    def verify(self, solution: Solution) -> bool:
        pass


# Constraint for total sum value
class TotalSumConstraint(Constraint):
    def __init__(self, expected_sum: int):
        self.expected_sum = expected_sum

    def verify(self, solution: Solution) -> bool:
        return solution.total_sum == self.expected_sum


# Constraint for central sum value
class CentralSumConstraint(Constraint):
    def __init__(self, expected_sum: int):
        self.expected_sum = expected_sum

    def verify(self, solution: Solution) -> bool:
        return sum(n.digit for n in solution.numbers[1:4]) == self.expected_sum


# Constraint for third digit (greater than 4 or net)
class Digit3Constraint(Constraint):
    def __init__(self, greater: bool):
        self.greater = greater

    def verify(self, solution: Solution) -> bool:
        if self.greater:
            return solution.numbers[2].digit > 4
        else:
            return solution.numbers[2].digit <= 4


# Candidate solutions manager
class SolutionsManager:
    def __init__(self, non_candidates: List[Number]):
        # Remaining candidates
        self.candidates = list(ALL_NUMBERS)
        for non_candidate in non_candidates:
            self.candidates.remove(non_candidate)

    # Return all possible solutions
    def compute(self, constraints: List[Constraint]) -> List[Solution]:
        # Only 5 candidates?
        candidates_count = len(self.candidates)
        if candidates_count <= 5:
            return [Solution(self.candidates)]

        # Generate solutions
        matching_solutions = []
        for offset_1 in range(candidates_count - 5 + 1):
            for offset_2 in range(offset_1 + 1, candidates_count - 4 + 1):
                for offset_3 in range(offset_2 + 1, candidates_count - 3 + 1):
                    for offset_4 in range(offset_3 + 1, candidates_count - 2 + 1):
                        for offset_5 in range(offset_4 + 1, candidates_count - 1 + 1):
                            # Generate solution
                            solution = Solution(
                                [
                                    self.candidates[offset_1],
                                    self.candidates[offset_2],
                                    self.candidates[offset_3],
                                    self.candidates[offset_4],
                                    self.candidates[offset_5],
                                ]
                            )

                            # Verify constraints
                            if all(c.verify(solution) for c in constraints):
                                matching_solutions.append(solution)

        return matching_solutions


# Sample run
my_numbers = [Number(0, Color.BLACK), Number(0, Color.WHITE), Number(3, Color.WHITE), Number(4, Color.BLACK), Number(6, Color.WHITE)]
guessed_numbers = [Number(5, Color.GREEN)]
m = SolutionsManager(my_numbers + guessed_numbers)
s = m.compute(
    [
        TotalSumConstraint(22),
        Digit3Constraint(False),
        CentralSumConstraint(13),
    ]
)
print(f"Solution candidates count: {len(s)}\n")

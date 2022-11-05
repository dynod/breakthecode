from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set


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

    @property
    def rich_string(self) -> str:
        if self.color == Color.WHITE:
            return "bold white"
        elif self.color == Color.GREEN:
            return "bold green"
        else:
            return "black on white"

    def __repr__(self) -> str:
        return f"[{self.rich_string}]{self.digit}[/]"

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Number) and (self.digit == __o.digit) and (self.color == __o.color)

    def __hash__(self) -> int:
        return self.digit + self.color.value * 10


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


# Candidate solutionblack
@dataclass
class Solution:
    numbers: List[Number] = field(default_factory=list)

    def __repr__(self) -> str:
        return ",".join(map(str, self.numbers))

    def __eq__(self, __o: object) -> bool:
        # Check all solution numbers
        return (
            isinstance(__o, Solution) and (len(self.numbers) == len(__o.numbers)) and all(self.numbers[i] == __o.numbers[i] for i in range(len(self.numbers)))
        )

    def __hash__(self) -> int:
        # Sum all numbers hash
        return sum(n.__hash__() for n in self.numbers)


# Constraint for solution
class Constraint(ABC):
    @abstractmethod
    def verify(self, solution: Solution) -> bool:
        pass  # pragma: no cover


# Candidate solutions manager
class SolutionsManager:
    def __init__(self, non_candidates: List[Number]):
        # Remaining candidates
        self.candidates = list(ALL_NUMBERS)
        for non_candidate in non_candidates:
            self.candidates.remove(non_candidate)

    # Return all possible solutions
    def compute(self, constraints: List[Constraint]) -> Set[Solution]:
        # Only 5 candidates?
        candidates_count = len(self.candidates)
        if candidates_count <= 5:
            return [Solution(self.candidates)]

        # Generate solutions
        matching_solutions = set()
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
                                matching_solutions.add(solution)

        return matching_solutions

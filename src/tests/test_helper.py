# Test BreakTheCode helper
import logging
from typing import List

from pytest_multilog import TestHelper

from breakthecode.constraints import ColorConstraint, DiffConstraint, DigitConstraint, OddEvenConstraint, PairsConstraint, PositionConstraint, SumConstraint
from breakthecode.model import Color, Number, Solution, SolutionsManager


class TestBreakTheCode(TestHelper):
    def print_solutions(self, s: List[Solution]):
        logging.info("Found solutions:")
        for item in s:
            logging.info(" ".join([f"{n.digit}{n.color.name[0]}" for n in item.numbers]))

    def test_obvious(self):
        s = SolutionsManager(
            [
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
            ]
        ).compute([])
        self.print_solutions(s)
        assert len(s) == 1
        assert all(
            n in s[0].numbers for n in [Number(7, Color.WHITE), Number(8, Color.BLACK), Number(8, Color.WHITE), Number(9, Color.BLACK), Number(9, Color.WHITE)]
        )

    def test_helper1(self):
        # Give a try with sample input, successively with more and more constraints
        i = [Number(1, Color.WHITE), Number(3, Color.BLACK), Number(6, Color.BLACK), Number(7, Color.BLACK), Number(7, Color.WHITE)]
        m = SolutionsManager(i)

        # Add diff contraint
        c = [DiffConstraint(9)]
        s = m.compute(c)
        assert len(s) == 710
        for sample in i:
            assert sample not in s, f"Unexpected input in solution: {sample}"

        # Add sum contraint
        c.append(SumConstraint(23, 2))
        s = m.compute(c)
        assert len(s) == 75

        # Another sum constraint with color
        c.append(SumConstraint(14, 0, None, Color.WHITE))
        s = m.compute(c)
        assert len(s) == 9

        # Add even count constraint
        c.append(OddEvenConstraint(False, 3))
        s = m.compute(c)
        self.print_solutions(s)
        assert len(s) == 4

        # Check final solution
        assert Solution([Number(0, Color.BLACK), Number(5, Color.GREEN), Number(6, Color.WHITE), Number(8, Color.WHITE), Number(9, Color.BLACK)]) in s

    def test_helper2(self):
        # Give a try with sample input, successively with more and more constraints
        i = [Number(0, Color.BLACK), Number(0, Color.WHITE), Number(1, Color.WHITE), Number(3, Color.BLACK), Number(8, Color.BLACK), Number(5, Color.GREEN)]
        m = SolutionsManager(i)

        # Add sum contraint
        c = [SumConstraint(22, 2)]
        s = m.compute(c)
        assert len(s) == 278

        # Add pos contraint
        c.append(PositionConstraint(Number(5, Color.GREEN), 2))
        s = m.compute(c)
        assert len(s) == 30

        # Add even count constraint
        c.append(OddEvenConstraint(False, 3))
        s = m.compute(c)
        assert len(s) == 12

        # Add color constraint
        c.append(ColorConstraint(Color.WHITE, 3))
        s = m.compute(c)
        self.print_solutions(s)
        assert len(s) == 5

        # Check final solution
        assert Solution([Number(2, Color.WHITE), Number(4, Color.BLACK), Number(5, Color.GREEN), Number(8, Color.WHITE), Number(9, Color.WHITE)]) in s

    def test_helper3(self):
        # Give a try with sample input, successively with more and more constraints
        i = [Number(0, Color.BLACK), Number(0, Color.WHITE), Number(3, Color.WHITE), Number(4, Color.BLACK), Number(6, Color.WHITE)]
        m = SolutionsManager(i)

        # Add sum contraint
        c = [SumConstraint(22)]
        s = m.compute(c)
        assert len(s) == 141

        # Add digit contraint
        c.append(DigitConstraint(False))
        s = m.compute(c)
        assert len(s) == 92

        # Add central sum constraint contraint
        c.append(SumConstraint(13, 1, 3))
        s = m.compute(c)
        assert len(s) == 30

        # Add pairs constraint
        c.append(PairsConstraint(0))
        s = m.compute(c)
        self.print_solutions(s)
        assert len(s) == 24

        # Check final solution
        assert Solution([Number(1, Color.BLACK), Number(2, Color.BLACK), Number(4, Color.WHITE), Number(7, Color.BLACK), Number(8, Color.WHITE)]) in s

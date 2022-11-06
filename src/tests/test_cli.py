import logging
from argparse import ArgumentTypeError

from pytest_multilog import TestHelper

from breakthecode.__main__ import main
from breakthecode.cli import color_builder, digit_constraint_builder, number_builder, pos_constraint_builder, sum_constraint_builder
from breakthecode.model import Color


class TestCli(TestHelper):
    def print_output(self, capsys):
        out, err = capsys.readouterr()
        logging.info("stdout:")
        logging.info(out)
        logging.info("stderr:")
        logging.info(err)

    def test_cli1(self, capsys):
        assert main(["-r1W", "-r3B", "-r6B", "-r7B", "-r7W", "-d9", "-s23,2", "-s14,0,5,w", "-e3"]) == 4
        self.print_output(capsys)

    def test_cli2(self, capsys):
        assert main(["-r0B", "-r0W", "-r1W", "-r3B", "-r8B", "-r5", "-s22,2", "-p5,2", "-e3", "-w3"]) == 5
        self.print_output(capsys)

    def test_cli3(self, capsys):
        assert main(["-r0B", "-r0W", "-r3W", "-r4B", "-r6W", "-s22", "-D2<=4", "-s13,1,3", "-P0"]) == 24
        self.print_output(capsys)

    def test_color_builder(self):
        assert color_builder("W") == Color.WHITE
        assert color_builder("B") == Color.BLACK
        assert color_builder("g") == Color.GREEN
        try:
            color_builder("foo")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "Unknown color" in str(e)

    def test_number_builder(self):
        try:
            number_builder("foo")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "Invalid length" in str(e)
        try:
            number_builder("fo")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "not a digit" in str(e)
        try:
            number_builder("3")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "Invalid color" in str(e)

    def test_sum_builder(self):
        try:
            sum_constraint_builder("1,2,3,4,5,6,7")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "Invalid sum spec" in str(e)

    def test_pos_builder(self):
        try:
            pos_constraint_builder("1,2,3,4,5,6,7")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "Invalid pos spec" in str(e)
        try:
            pos_constraint_builder("2w,foo")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "Invalid position" in str(e)

    def test_digit_builder(self):
        try:
            digit_constraint_builder("1>2>3")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "Invalid comparison syntax" in str(e)
        try:
            digit_constraint_builder("foo")
            raise AssertionError("Shouldn't get here")
        except ArgumentTypeError as e:
            assert "Invalid comparison:" in str(e)

    def test_extra_constraints(self, capsys):
        assert main(["-r1W", "-r3B", "-r6B", "-r7B", "-r7W", "-d9", "-o3", "-b2"]) == 66
        self.print_output(capsys)

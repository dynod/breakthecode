import logging

from pytest_multilog import TestHelper

from breakthecode.__main__ import main


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
        assert main(["-r0B", "-r0W", "-r3W", "-r4B", "-r6W", "-s22", "-D2<=4", "-s13,1,3", "-P0"]) == 30
        self.print_output(capsys)

import sys

from breakthecode.cli import HelperCli


def main() -> int:  # pragma: no cover
    return HelperCli(sys.argv[1:]).run()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

import sys
from typing import List

from breakthecode.cli import HelperCli


def main(args: List[str]) -> int:
    return HelperCli(args).run()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from functools import reduce
from pathlib import Path

from kankei.utils import read_table


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "tables", metavar="TABLE", nargs="*", type=Path, default=sys.stdin
    )
    parser.add_argument("-o", "--on", type=str, action="append")
    args = parser.parse_args()

    dfs = (read_table(t) for t in args.tables)
    joined = reduce(lambda lhs, rhs: lhs.merge(rhs, on=args.on), dfs)

    sys.stdout.write(joined.drop_duplicates().to_csv(index=False))


if __name__ == "__main__":
    main()

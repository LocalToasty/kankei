#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

from tabulate import tabulate

from kankei.utils import read_table


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "table", metavar="TABLE", type=str, nargs="?", default=sys.stdin
    )
    args = parser.parse_args()

    df = read_table(args.table, dtype=None)
    sys.stdout.write(tabulate(df, headers="keys", showindex=False))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
from pathlib import Path

from kankei.utils import read_table


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "table", metavar="TABLE", type=Path, nargs="?", default=sys.stdin
    )
    parser.add_argument(
        "-c", "--column", type=str, dest="columns", action="append", default=[]
    )
    args = parser.parse_args()

    df = read_table(args.table)
    projection = df[args.columns]
    sys.stdout.write(projection.drop_duplicates().to_csv(index=False))


if __name__ == "__main__":
    main()

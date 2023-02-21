#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from pathlib import Path

from kankei.utils import read_table


def main():
    parser = ArgumentParser(description="Renames a column in a table.")
    parser.add_argument(
        "table",
        metavar="TABLE",
        type=Path,
        nargs="?",
        default=sys.stdin,
        help="File to read from, or stdin if not specified.",
    )
    parser.add_argument(
        "-r",
        "--rename",
        metavar=("OLD", "NEW"),
        nargs=2,
        type=str,
        dest="renamings",
        action="append",
        default=[],
        help=(
            "Renames a column. "
            "Can be specified multiple times to rename multiple columns."
        ),
    )
    args = parser.parse_args()

    df = read_table(args.table)

    renamed = df.rename(columns=dict(args.renamings))

    sys.stdout.write(renamed.drop_duplicates().to_csv(index=False))


if __name__ == "__main__":
    main()

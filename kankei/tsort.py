#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

from kankei.utils import read_table


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "table", metavar="TABLE", type=str, nargs="?", default=sys.stdin
    )
    parser.add_argument(
        "-b",
        "--by",
        type=str,
        action="append",
        required=True,
        help="Column to sort by.  Can be specified multiple times.",
    )
    order_group = parser.add_mutually_exclusive_group()
    order_group.add_argument(
        "-a", "--ascending", dest="ascending", action="store_true", default=True
    )
    order_group.add_argument(
        "-d", "--descending", dest="ascending", action="store_false"
    )
    args = parser.parse_args()

    df = read_table(args.table)
    sorted = df.sort_values(by=args.by, ascending=args.ascending)
    sys.stdout.write(sorted.to_csv(index=False))


if __name__ == "__main__":
    main()

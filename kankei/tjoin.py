#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from functools import reduce
from pathlib import Path

from kankei.utils import (
    add_general_arguments,
    post_process_table,
    read_table,
    write_table,
)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "tables", metavar="TABLE", nargs="*", type=Path, default=sys.stdin
    )
    parser.add_argument("-o", "--on", type=str, action="append")
    parser = add_general_arguments(parser)
    args = parser.parse_args()

    dfs = (read_table(t, dtype=str, renamings=args.renamings) for t in args.tables)
    joined = reduce(lambda lhs, rhs: lhs.merge(rhs, on=args.on), dfs)

    write_table(
        post_process_table(
            joined,
            project_onto=args.project_onto,
            unique=args.unique,
            sort_by=args.sort_by,
            sort_ascending=args.sort_ascending,
            offset=args.offset,
            limit=args.limit,
        ),
        pretty_print=args.pretty_print,
    )


if __name__ == "__main__":
    main()

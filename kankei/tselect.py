#!/usr/bin/env python3
import operator
import re
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Callable, Union

import pandas as pd

from kankei.utils import (
    add_general_arguments,
    post_process_table,
    read_table,
    write_table,
)


@dataclass
class AttributeName:
    v: str


optable = {
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    ">": operator.gt,
}


@dataclass
class Predicate:
    lhs: AttributeName
    op: Callable
    rhs: Union[AttributeName, str, float]

    def get_selected_idxs(self, df: pd.DataFrame) -> pd.Series:
        if isinstance(self.rhs, AttributeName):
            return self.op(df[self.lhs.v], df[self.rhs.v])
        else:
            return self.op(df[self.lhs.v], self.rhs)

    @classmethod
    def from_str(cls, s: str):
        match = re.match(r"^(.+)(<|<=|!=|==|>=|>)(.+)$", s)
        if not match:
            raise ValueError(f"could not parse selection {s}")

        raw_lhs, raw_op, raw_rhs = match.groups()
        lhs = AttributeName(raw_lhs)
        op = optable[raw_op]

        if raw_rhs[0] == '"' and raw_rhs[-1] == '"':
            rhs = raw_rhs[1:-1]
        else:
            try:
                rhs = float(raw_rhs)
            except ValueError:
                rhs = AttributeName(raw_rhs)

        return cls(lhs, op, rhs)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "table",
        metavar="TABLE",
        type=Path,
        nargs="?",
        default=sys.stdin,
        help="File to read from, or stdin if not specified.",
    )
    parser.add_argument(
        "-s",
        "--select",
        metavar="PRED",
        dest="predicates",
        type=Predicate.from_str,
        action="append",
        default=[],
        help=(
            "A predicate of the form '<COL><OP><COL OR VAL>', "
            "where COL is a column name, "
            "OP is one of '<', '<=', '==', '!=', '>=' and '>', "
            "and VAL is a number or a string enclosed in double quotes. "
            "Can be given multiple times, "
            "in which case all rows fulfilling any of the predicates "
            "will be selected."
        ),
    )
    parser.add_argument(
        "--raw", action="store_true", help="Always interpret values as strings."
    )
    parser = add_general_arguments(parser)
    args = parser.parse_args()

    df = read_table(
        args.table, dtype=str if args.raw else None, renamings=args.renamings
    )

    selected_idxs = reduce(
        operator.or_,
        (pred.get_selected_idxs(df) for pred in args.predicates),
        [False] * len(df),
    )

    write_table(
        post_process_table(
            df[selected_idxs],
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

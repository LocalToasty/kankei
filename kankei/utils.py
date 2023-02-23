import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, Sequence, Tuple, Type

import pandas as pd
from tabulate import tabulate

all = ["add_general_arguments", "read_table", "post_process_table", "write_table"]


def add_general_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "-r",
        "--rename",
        metavar=("OLD", "NEW"),
        nargs=2,
        type=str,
        dest="renamings",
        action="append",
        help=(
            "Renames a column. "
            "Can be specified multiple times to rename multiple columns."
        ),
    )

    parser.add_argument(
        "-u",
        "--unique",
        action="store_true",
        help="Remove duplicate entries.",
    )

    parser.add_argument(
        "-b",
        "--sort-by",
        type=str,
        default=None,
        action="append",
        help="Column to sort by. Can be specified multiple times.",
    )
    order_group = parser.add_mutually_exclusive_group()
    order_group.add_argument(
        "-a", "--ascending", dest="sort_ascending", action="store_true", default=True
    )
    order_group.add_argument(
        "-d", "--descending", dest="sort_ascending", action="store_false"
    )

    parser.add_argument(
        "-c",
        "--column",
        type=str,
        dest="project_onto",
        action="append",
        default=None,
        help="Restrict output to this column. Can be given multiple times.",
    )

    parser.add_argument(
        "-o",
        "--offset",
        metavar="N",
        type=int,
        default=0,
        help="Skip the first N rows of the output.",
    )

    parser.add_argument(
        "-l",
        "--limit",
        metavar="N",
        type=int,
        help="Only output N results.",
    )

    parser.add_argument(
        "-p",
        "--pretty",
        dest="pretty_print",
        action="store_true",
        help="Pretty-print the output.",
    )
    return parser


def read_table(
    file, dtype: Type, renamings: Optional[Sequence[Tuple[str, str]]]
) -> pd.DataFrame:
    if isinstance(file, Path) and file.suffix == ".xlsx":
        df = pd.read_excel(file, dtype=dtype)
    elif isinstance(file, Path) and file == "-":
        df = pd.read_csv(sys.stdin, dtype=dtype)
    else:
        df = pd.read_csv(file, dtype=dtype)

    if renamings is not None:
        df = df.rename(columns=dict(renamings))

    return df


def post_process_table(
    df: pd.DataFrame,
    project_onto: Optional[Sequence[str]],
    unique: bool,
    sort_by: Optional[Sequence[str]],
    sort_ascending: bool,
    offset: int,
    limit: Optional[int],
) -> pd.DataFrame:
    if project_onto is not None:
        df = df[project_onto]
    if unique:
        df = df.drop_duplicates()
    if sort_by is not None:
        df = df.sort_values(sort_by, ascending=sort_ascending)

    df = df.iloc[offset:]
    if limit is not None:
        df = df.iloc[:limit]

    return df


def write_table(df: pd.DataFrame, pretty_print: bool) -> None:
    if pretty_print:
        sys.stdout.write(tabulate(df, headers="keys", showindex=False))
        sys.stdout.write("\n")
    else:
        sys.stdout.write(df.to_csv(index=False))

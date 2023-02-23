#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

from kankei.utils import read_table


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "tables", metavar="TABLE", nargs="*", type=Path, default=[sys.stdin]
    )
    args = parser.parse_args()

    dfs = (read_table(t) for t in args.tables)
    concatenated = pd.concat(dfs)

    sys.stdout.write(concatenated.drop_duplicates().to_csv(index=False))


if __name__ == "__main__":
    main()

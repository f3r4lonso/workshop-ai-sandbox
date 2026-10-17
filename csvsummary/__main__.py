import argparse
import sys

from .stats import format_summary, read_rows, summarize


def main(argv=None):
    parser = argparse.ArgumentParser(prog="csvsummary", description="Print count, mean and median per numeric column.")
    parser.add_argument("path", help="CSV file with a header row")
    args = parser.parse_args(argv)
    print(format_summary(summarize(read_rows(args.path))))
    return 0


if __name__ == "__main__":
    sys.exit(main())

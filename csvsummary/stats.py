"""Summary statistics for the numeric columns of a CSV file."""

import csv
import statistics


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def numeric_columns(rows):
    """Columns whose every value parses as a number, in file order."""
    columns = list(rows[0].keys())
    return [c for c in columns if all(is_number(row[c]) for row in rows)]


def summarize(rows):
    """{column: {"count", "mean", "median"}} for each numeric column."""
    result = {}
    for column in numeric_columns(rows):
        values = [float(row[column]) for row in rows]
        result[column] = {
            "count": len(values),
            "mean": statistics.fmean(values),
            "median": statistics.median(values),
        }
    return result


def format_summary(summary):
    lines = []
    for column, stats in summary.items():
        lines.append(f"{column}: count={stats['count']} mean={stats['mean']:.2f} median={stats['median']:.2f}")
    return "\n".join(lines)

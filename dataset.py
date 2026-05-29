"""
Module for loading and summarising the practice dataset.

On import this module exposes the global variable ``df`` containing the
contents of ``dataset.csv`` as a :class:`pandas.DataFrame`.  No output
is produced when the module is imported.  When executed directly from
the command line (``python dataset.py``) the script prints a summary
of the dataset to the console and writes the same summary into
``report.txt`` using UTF‑8 encoding.

The summary includes:

* The shape of the dataset (rows, columns).
* The dataframe info (column types and non‑null counts).
* The number of missing values per column (even when zero).
* Basic statistics (mean, median and standard deviation) for each
  quantitative column.
* Unique values and their frequencies for each categorical column.

Quantitative and categorical columns are defined according to the
specification provided with the assignment: columns that store counts
or measurements are considered quantitative, while columns encoding
categories (even if represented as integers) are considered
categorical.  The technical index column ``Unnamed: 0`` is excluded
from the analysis.

Usage:
    python dataset.py
"""

from __future__ import annotations

import os
from pathlib import Path
import pandas as pd

# Determine the location of this file and construct the path to the CSV.
_BASE_DIR = Path(__file__).resolve().parent
_DATASET_PATH = _BASE_DIR / "dataset.csv"

# Load the dataset into a global DataFrame.  Using a relative path
# makes it portable when imported from another module.
df: pd.DataFrame = pd.read_csv(_DATASET_PATH)

def _summarise_dataset(data: pd.DataFrame) -> str:
    """Return a string with a detailed summary of the dataset.

    The summary includes the shape, info, missing values, basic
    statistics for quantitative columns and value counts for
    categorical columns.  The technical index column is ignored in
    these analyses.

    Args:
        data: The DataFrame to summarise.

    Returns:
        A formatted multi‑line string with the summary.
    """
    lines: list[str] = []

    # Shape of the dataset
    lines.append(str(data.shape))

    # Capture DataFrame info into a buffer
    from io import StringIO
    buffer = StringIO()
    data.info(buf=buffer)
    lines.append(buffer.getvalue().rstrip())

    # Missing values per column
    missing_counts = data.isna().sum()
    for col, missing in missing_counts.items():
        lines.append(f"{col}\t{missing}")

    # Define technical, quantitative and categorical columns
    technical_cols = ["Unnamed: 0"]
    quantitative_cols = [
        "platelets",
        "serum creatinine",
        "serum sodium",
        "creatinine phosphokinase",
        "ejection fraction",
    ]
    categorical_cols = ["sex", "smoking", "death"]

    # Basic statistics for quantitative columns
    lines.append("Колонка>\tсреднее\tмедиана\tотклонение")
    for col in quantitative_cols:
        series = data[col].dropna()
        mean_val = series.mean()
        median_val = series.median()
        std_val = series.std()
        # Format to two decimal places
        lines.append(
            f"{col}>\t{mean_val:.2f};\t{median_val:.2f};\t{std_val:.2f}"
        )

    # Value counts for categorical columns
    for col in categorical_cols:
        vc = data[col].value_counts()
        # Each category and its count on its own line
        lines.append(col)
        for value, count in vc.items():
            lines.append(f"{value}\t{count}")
        # Show the pandas dtype for completeness as in the example
        lines.append(f"Name: count, dtype: {vc.dtype}")

    return "\n".join(lines)


def _write_report(content: str, filename: str = "report.txt") -> None:
    """Write summary content to a UTF‑8 encoded text file.

    Args:
        content: The text content to write.
        filename: The file name to write to (relative to _BASE_DIR).
    """
    report_path = _BASE_DIR / filename
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    """Entry point for command line execution.

    Generates a summary of ``df`` and prints it to the console and
    writes the same output to ``report.txt``.  Importing this
    module does not trigger any printing or file output.
    """
    summary = _summarise_dataset(df)
    print(summary)
    _write_report(summary)


if __name__ == "__main__":
    main()

import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the source workbook location
RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "SY 2023-2024 School Level Data on Official Enrollment 13.xlsx"
)


def load_data(file_path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Load the school-level enrollment dataset from the DB worksheet.

    Args:
        file_path: Path to the original Excel workbook.

    Returns:
        pd.DataFrame: Extracted school-level enrollment records.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source workbook not found: {file_path}"
        )

    try:
        data = pd.read_excel(
            file_path,
            sheet_name="DB",
            header=4
        )

    except ValueError as error:
        raise ValueError(
            f"Unable to read the DB worksheet: {error}"
        ) from error

    # Validate extracted dataset dimensions
    expected_rows = 60167
    expected_columns = 72

    if data.shape != (expected_rows, expected_columns):
        raise ValueError(
            f"Unexpected dataset dimensions. "
            f"Expected {(expected_rows, expected_columns)}, "
            f"but received {data.shape}."
        )

    return data
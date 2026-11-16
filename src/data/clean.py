from pathlib import Path

import numpy as np
import pandas as pd

from src.data.load import load_data

# Load original dataset
df = load_data()

# =============================================
# Standardize Missing Values and Placeholders
# =============================================

# Missing values and placeholders (From Dataset Audit)
PLACEHOLDERS = [ 
    "-",
    "none",
    "not applicable",
    "-n/a",
    "-none",
    "n/a",
    "na",
    "null",
    "nil",
    ""
]

def standardize_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert recognized Street Address placeholders into missing values.
    """

    df_standard = df.copy()

    column = "Street Address"

    if column not in df.columns:
        raise KeyError(f"Required column not found: {column}")

    # Normalize values temporarily for comparison
    normalized = (
        df_standard[column]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Replace recognized placeholders with missing values
    df_standard[column] = df_standard[column].mask(
        normalized.isin(PLACEHOLDERS),
        np.nan
    )

    return df_standard

df_standard = standardize_missing_values(df)

print("Missing values before cleaning:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print("Missing values after cleaning:")
print(df_standard.isnull().sum()[df_standard.isnull().sum() > 0])

# =============================================
# Standardize Text Values
# =============================================

def standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading and trailing whitespace from text columns.
    Preserve non-string values and existing missing values.
    """

    df_standard = df.copy()

    text_columns = df_standard.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        df_standard[column] = df_standard[column].map(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

    return df_standard

df_text = standardize_text(df_standard)
print("\nText standardization complete.")

# =============================================
# Post-Cleaning Validation
# =============================================

# Check dataset dimensions
assert df_text.shape == df.shape, (
    "Dataset dimensions changed unexpectedly."
)

enrollment_columns = [
    column for column in df_text.columns
    if column.endswith(" Male") or column.endswith(" Female")
]

# Check dataset dimensions
assert df_text.shape == df.shape, (
    "Dataset dimensions changed unexpectedly."
)

# Identify enrollment columns
enrollment_columns = [
    column for column in df_text.columns
    if column.endswith(" Male") or column.endswith(" Female")
]

# Check expected number of enrollment columns
assert len(enrollment_columns) == 58, (
    f"Expected 58 enrollment columns, "
    f"but found {len(enrollment_columns)}."
)

# Check that enrollment columns remain numeric
non_numeric_columns = [
    column for column in enrollment_columns
    if not pd.api.types.is_numeric_dtype(df_text[column])
]

assert not non_numeric_columns, (
    f"Non-numeric enrollment columns found: {non_numeric_columns}"
)

# Check that enrollment values remain nonnegative
negative_values = (
    df_text[enrollment_columns] < 0
).sum().sum()

assert negative_values == 0, (
    f"Found {negative_values} negative enrollment values."
)

# Check missing enrollment values
missing_enrollment = (
    df_text[enrollment_columns].isna().sum().sum()
)

assert missing_enrollment == 0, (
    f"Found {missing_enrollment} missing enrollment values."
)

# Check total enrollment remains unchanged
original_total = df[enrollment_columns].sum().sum()
cleaned_total = df_text[enrollment_columns].sum().sum()

assert original_total == cleaned_total, (
    "Total enrollment changed during cleaning."
)

# Display validation results
print("\nPOST-CLEANING VALIDATION")
print("--------------------------------")
print(f"Dataset dimensions: {df_text.shape}")
print(f"Enrollment columns: {len(enrollment_columns)}")
print(f"Non-numeric enrollment columns: {len(non_numeric_columns)}")
print(f"Missing enrollment values: {missing_enrollment}")
print(f"Negative enrollment values: {negative_values}")
print(f"Original total enrollment: {original_total:,}")
print(f"Cleaned total enrollment: {cleaned_total:,}")

print("\nMissing values after cleaning:")
print(df_text.isnull().sum()[df_text.isnull().sum() > 0])

print("\nAll post-cleaning validation checks passed!")

# =============================================
# Save the cleaned dataset
# =============================================
# Get the project root directory
PROJECT_ROOT = Path.cwd()

# Define the output directory
output_directory = PROJECT_ROOT / "data" / "interim"

# Create the directory if it doesn't exist
output_directory.mkdir(parents=True, exist_ok=True)

# Define the output file
output_path = output_directory / "school_records_cleaned.parquet"

# Save the cleaned dataset
df_text.to_parquet(
    output_path,
    index=False,
    engine="pyarrow"
)
print("\nCleaned dataset saved successfully!")
print(f"File location: {output_path}")
print(f"Dataset dimensions: {df_text.shape}")
print(f"File size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")

# =============================================
# Check saving and loading of Parquet file
# =============================================

# Load the saved Parquet file
df_saved = pd.read_parquet(output_path)

# Verify dimensions
assert df_saved.shape == df_text.shape

# Verify enrollment totals
assert (
    df_saved[enrollment_columns].sum().sum()
    == df_text[enrollment_columns].sum().sum()
)

# Verify column names and order
assert df_saved.columns.tolist() == df_text.columns.tolist()

print("Parquet verification successful!")
print(f"Saved dataset shape: {df_saved.shape}")
print(f"Total enrollment: {df_saved[enrollment_columns].sum().sum():,}")

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLEANED_DATA_PATH = (
    PROJECT_ROOT / "data" / "interim" / "school_records_cleaned.parquet"
)

SCHOOL_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "school_enrollment.parquet"
)

LONG_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "enrollment_long.parquet"
)

EXPECTED_SCHOOLS = 60167
EXPECTED_ENROLLMENT_COLUMNS = 58
EXPECTED_SCHOOL_COLUMNS = 83
EXPECTED_LONG_ROWS = 3489686
EXPECTED_LONG_COLUMNS = 23
EXPECTED_ZERO_SCHOOLS = 115
EXPECTED_TOTAL_ENROLLMENT = 27081292

# =============================================
# Add a function to load the prepared datasets
# =============================================

def load_prepared_datasets():
    """
    Load the cleaned source and prepared enrollment datasets.

    Returns:
        tuple: Cleaned source, school-level dataset,
        and long-format dataset.
    """

    paths = [
        CLEANED_DATA_PATH,
        SCHOOL_DATA_PATH,
        LONG_DATA_PATH,
    ]

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(
                f"Required dataset not found: {path}"
            )

    cleaned = pd.read_parquet(CLEANED_DATA_PATH)
    school = pd.read_parquet(SCHOOL_DATA_PATH)
    long = pd.read_parquet(LONG_DATA_PATH)

    return cleaned, school, long

# =============================================
# Add structural validation
# =============================================


def validate_structure(cleaned, school, long):
    """
    Validate dataset dimensions and original column preservation.
    """

    assert cleaned.shape == (EXPECTED_SCHOOLS, 72), (
        f"Unexpected cleaned dataset shape: {cleaned.shape}"
    )

    assert school.shape == (
        EXPECTED_SCHOOLS,
        EXPECTED_SCHOOL_COLUMNS,
    ), f"Unexpected school dataset shape: {school.shape}"

    assert long.shape == (
        EXPECTED_LONG_ROWS,
        EXPECTED_LONG_COLUMNS,
    ), f"Unexpected long dataset shape: {long.shape}"

    missing_columns = set(cleaned.columns) - set(school.columns)

    assert not missing_columns, (
        f"Original columns missing from school output: "
        f"{missing_columns}"
    )

    print("Structural validation passed!")

# =============================================
# Add School ID validation
# =============================================


def validate_school_ids(cleaned, school, long):
    """
    Validate school ID uniqueness and preservation.
    """

    assert cleaned["BEIS School ID"].is_unique, (
        "Duplicate BEIS School IDs found in cleaned source."
    )

    assert school["BEIS School ID"].is_unique, (
        "Duplicate BEIS School IDs found in school output."
    )

    source_ids = set(cleaned["BEIS School ID"])
    school_ids = set(school["BEIS School ID"])
    long_ids = set(long["BEIS School ID"])

    assert source_ids == school_ids, (
        "School IDs do not match between cleaned source "
        "and school output."
    )

    assert source_ids == long_ids, (
        "School IDs do not match between cleaned source "
        "and long-format output."
    )

    print("School ID validation passed!")

# =============================================
# Validate overall, male, and female enrollment
# =============================================


def validate_enrollment_totals(cleaned, school, long):
    """
    Validate overall, male, and female enrollment totals.
    """

    enrollment_columns = [
        column for column in cleaned.columns
        if column.endswith(" Male") or column.endswith(" Female")
    ]

    male_columns = [
        column for column in enrollment_columns
        if column.endswith(" Male")
    ]

    female_columns = [
        column for column in enrollment_columns
        if column.endswith(" Female")
    ]

    source_total = cleaned[enrollment_columns].to_numpy().sum()
    source_male = cleaned[male_columns].to_numpy().sum()
    source_female = cleaned[female_columns].to_numpy().sum()

    school_total = school["Total Enrollment"].sum()
    school_male = school["Male Enrollment"].sum()
    school_female = school["Female Enrollment"].sum()

    long_total = long["Enrollment"].sum()

    assert source_total == EXPECTED_TOTAL_ENROLLMENT
    assert source_total == school_total == long_total

    assert source_male == school_male
    assert source_female == school_female

    assert school_male + school_female == school_total

    print("Enrollment total validation passed!")

# =============================================
# Validate education-level totals
# =============================================


def validate_education_totals(cleaned, school):
    """
    Validate Kindergarten, Elementary, JHS, and SHS totals.
    """

    education_columns = {
        "Kindergarten Enrollment": [
            column for column in cleaned.columns
            if column.startswith("K ")
        ],
        "Elementary Enrollment": [
            column for column in cleaned.columns
            if (
                column.startswith(
                    ("G1 ", "G2 ", "G3 ", "G4 ", "G5 ", "G6 ")
                )
                or column.startswith("Elem NG ")
            )
        ],
        "Junior High School Enrollment": [
            column for column in cleaned.columns
            if (
                column.startswith(("G7 ", "G8 ", "G9 ", "G10 "))
                or column.startswith("JHS NG ")
            )
        ],
        "Senior High School Enrollment": [
            column for column in cleaned.columns
            if column.startswith(("G11 ", "G12 "))
        ],
    }

    for measure, columns in education_columns.items():
        source_total = cleaned[columns].to_numpy().sum()
        output_total = school[measure].sum()

        assert source_total == output_total, (
            f"Education total mismatch for {measure}: "
            f"source={source_total}, output={output_total}"
        )

    assert sum(
        school[column].sum()
        for column in education_columns
    ) == school["Total Enrollment"].sum()

    print("Education-level validation passed!")

# =============================================
# Validate grade-level totals
# =============================================


def validate_grade_totals(long):
    """
    Validate enrollment totals for each grade level.
    """

    expected_totals = {
        "K": 2047356,
        "G1": 2161371,
        "G2": 2205979,
        "G3": 2183377,
        "G4": 2029448,
        "G5": 2309827,
        "G6": 2183355,
        "Elem NG": 81238,
        "G7": 1808212,
        "G8": 1940033,
        "G9": 1992251,
        "G10": 2004570,
        "JHS NG": 4199,
        "G11": 209250 + 553826 + 397927 + 285399
               + 2684 + 628861 + 3896 + 8223,
        "G12": 221212 + 531111 + 357783 + 327108
               + 2639 + 588691 + 3659 + 7807,
    }

    actual_totals = (
        long.groupby("Grade Level")["Enrollment"]
        .sum()
        .to_dict()
    )

    assert actual_totals == expected_totals, (
        "Grade-level enrollment totals do not match "
        "the expected values."
    )

    print("Grade-level validation passed!")

# =============================================
# Validate SHS strand and track totals
# =============================================


def validate_shs_totals(long):
    """
    Validate SHS strand and track enrollment totals.
    """

    expected_strands = {
        "ABM": 430462,
        "HUMSS": 1084937,
        "STEM": 755710,
        "GAS": 612507,
        "PBM": 5323,
    }

    expected_tracks = {
        "Academic": 2888939,
        "TVL": 1217552,
        "Sports": 7555,
        "Arts": 16030,
    }

    actual_strands = (
        long.dropna(subset=["SHS Strand"])
        .groupby("SHS Strand")["Enrollment"]
        .sum()
        .to_dict()
    )

    actual_tracks = (
        long.dropna(subset=["SHS Track"])
        .groupby("SHS Track")["Enrollment"]
        .sum()
        .to_dict()
    )

    assert actual_strands == expected_strands, (
        "SHS strand totals do not match expected values."
    )

    assert actual_tracks == expected_tracks, (
        "SHS track totals do not match expected values."
    )

    assert sum(actual_tracks.values()) == 4130076

    print("SHS strand and track validation passed!")

# =============================================
# Add invalid-value validation
# =============================================


def validate_enrollment_values(cleaned, long):
    """
    Check for negative, missing, and non-finite enrollment values.
    """

    enrollment_columns = [
        column for column in cleaned.columns
        if column.endswith(" Male") or column.endswith(" Female")
    ]

    negative_source = (
        cleaned[enrollment_columns] < 0
    ).to_numpy().sum()

    negative_long = (long["Enrollment"] < 0).sum()

    missing_source = (
        cleaned[enrollment_columns].isna()
    ).to_numpy().sum()

    missing_long = long["Enrollment"].isna().sum()

    non_finite_long = (
        ~np.isfinite(long["Enrollment"])
    ).sum()

    assert negative_source == 0
    assert negative_long == 0
    assert missing_source == 0
    assert missing_long == 0
    assert non_finite_long == 0

    print("Enrollment value validation passed!")

# =============================================
# Validate zero-enrollment school retention
# =============================================


def validate_zero_enrollment(cleaned, school):
    """
    Confirm that all zero-enrollment schools are retained.
    """

    enrollment_columns = [
        column for column in cleaned.columns
        if column.endswith(" Male") or column.endswith(" Female")
    ]

    source_totals = (
        cleaned.set_index("BEIS School ID")[enrollment_columns]
        .sum(axis=1)
    )

    source_zero_ids = set(
        source_totals[source_totals == 0].index
    )

    output_zero_ids = set(
        school.loc[
            school["Zero Enrollment Flag"],
            "BEIS School ID"
        ]
    )

    assert source_zero_ids == output_zero_ids, (
        "Zero-enrollment school IDs do not match."
    )

    assert len(source_zero_ids) == EXPECTED_ZERO_SCHOOLS

    assert (
        school["Zero Enrollment Flag"]
        == (school["Total Enrollment"] == 0)
    ).all()

    print("Zero-enrollment validation passed!")

# =============================================
# Validate long-format record counts
# =============================================


def validate_long_records(cleaned, long):
    """
    Confirm that every school has 58 enrollment records.
    """

    records_per_school = long.groupby(
        "BEIS School ID"
    ).size()

    assert len(records_per_school) == EXPECTED_SCHOOLS

    assert (
        records_per_school == EXPECTED_ENROLLMENT_COLUMNS
    ).all(), "Some schools do not have exactly 58 records."

    expected_rows = (
        EXPECTED_SCHOOLS * EXPECTED_ENROLLMENT_COLUMNS
    )

    assert len(long) == expected_rows

    print("Long-format record validation passed!")

# =============================================
# Validate missing-value preservation
# =============================================


def validate_missing_values(cleaned, school):
    """
    Confirm expected missing-value counts are preserved.
    """

    expected_missing = {
        "Street Address": 5291,
        "Barangay": 70,
    }

    for column, expected_count in expected_missing.items():
        source_count = cleaned[column].isna().sum()
        output_count = school[column].isna().sum()

        assert source_count == expected_count, (
            f"Unexpected missing count in cleaned source: {column}"
        )

        assert output_count == expected_count, (
            f"Missing count changed in school output: {column}"
        )

    zero_schools = school["Total Enrollment"] == 0

    assert (
        school.loc[zero_schools, "Male Enrollment Share (%)"].isna()
    ).all()

    assert (
        school.loc[zero_schools, "Female Enrollment Share (%)"].isna()
    ).all()

    print("Missing-value validation passed!")

# =============================================
# Create one function to run all validations
# =============================================

def run_all_validations():
    """
    Load datasets and execute all validation checks.
    """

    print("=" * 55)
    print("EDUINSIGHT DATA VALIDATION")
    print("=" * 55)

    cleaned, school, long = load_prepared_datasets()

    print("\n[1] STRUCTURAL VALIDATION")
    validate_structure(cleaned, school, long)

    print("\n[2] SCHOOL ID VALIDATION")
    validate_school_ids(cleaned, school, long)

    print("\n[3] NUMERICAL VALIDATION")
    validate_enrollment_totals(cleaned, school, long)
    validate_education_totals(cleaned, school)
    validate_grade_totals(long)
    validate_shs_totals(long)
    validate_enrollment_values(cleaned, long)

    print("\n[4] RECORD VALIDATION")
    validate_zero_enrollment(cleaned, school)
    validate_long_records(cleaned, long)
    validate_missing_values(cleaned, school)

    print("\n" + "=" * 55)
    print("ALL DATA VALIDATION CHECKS PASSED!")
    print("=" * 55)

if __name__ == "__main__":
    run_all_validations()
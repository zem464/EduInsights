import pandas as pd
from pathlib import Path

# =============================================
# Project Paths
# =============================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "school_records_cleaned.parquet"
)

OUTPUT_DIRECTORY = PROJECT_ROOT / "data" / "processed"

# =============================================
# Identify Enrollment Columns
# =============================================

def get_enrollment_columns(df: pd.DataFrame) -> list[str]:
    """
    Identify the 58 male and female enrollment columns.
    """

    return [
        column for column in df.columns
        if column.endswith(" Male") or column.endswith(" Female")
    ]

def get_metadata_columns(
    df: pd.DataFrame,
    enrollment_columns: list[str]
) -> list[str]:
    """
    Identify school metadata columns by excluding
    enrollment columns.
    """

    return [
        column for column in df.columns
        if column not in enrollment_columns
    ]

# =============================================
# School-Level Analytical Dataset
# =============================================

def create_school_enrollment(
    df: pd.DataFrame,
    enrollment_columns: list[str]
) -> pd.DataFrame:
    """
    Create a school-level analytical dataset.

    Preserves all original school metadata and enrollment
    columns, then adds male, female, and total enrollment.
    """

    school_enrollment = df.copy()

    # Separate male and female enrollment columns
    male_columns = [
        column for column in enrollment_columns
        if column.endswith(" Male")
    ]

    female_columns = [
        column for column in enrollment_columns
        if column.endswith(" Female")
    ]

    # Calculate enrollment totals per school
    school_enrollment["Male Enrollment"] = (
        school_enrollment[male_columns].sum(axis=1)
    )

    school_enrollment["Female Enrollment"] = (
        school_enrollment[female_columns].sum(axis=1)
    )

    school_enrollment["Total Enrollment"] = (
        school_enrollment["Male Enrollment"]
        + school_enrollment["Female Enrollment"]
    )

    return school_enrollment

# =============================================
# Long-Format Enrollment Dataset
# =============================================

def create_enrollment_long(
    df: pd.DataFrame,
    enrollment_columns: list[str],
    metadata_columns: list[str]
) -> pd.DataFrame:
    """
    Reshape enrollment columns into long format.

    Each row represents one school's enrollment
    for a specific category and sex.
    """

    enrollment_long = df.melt(
        id_vars=metadata_columns,
        value_vars=enrollment_columns,
        var_name="Enrollment Field",
        value_name="Enrollment"
    )

    # Remove sex from the original column name
    enrollment_long["Enrollment Category"] = (
        enrollment_long["Enrollment Field"]
        .str.replace(
            r"\s+(Male|Female)$",
            "",
            regex=True
        )
    )

    # Extract sex
    enrollment_long["Sex"] = (
        enrollment_long["Enrollment Field"]
        .str.extract(r"\s+(Male|Female)$")[0]
    )

    # Remove the temporary combined field
    enrollment_long = enrollment_long.drop(
        columns=["Enrollment Field"]
    )

    # Extract grade level
    enrollment_long["Grade Level"] = (
        enrollment_long["Enrollment Category"]
        .str.extract(
            r"^(Elem NG|JHS NG|K|G(?:1[0-2]|[1-9]))"
        )[0]
    )

    # Classify education level
    enrollment_long["Education Level"] = (
        enrollment_long["Grade Level"]
        .map({
            "K": "Kindergarten",
            "Elem NG": "Elementary",
            "JHS NG": "Junior High School"
        })
    )

    # Classify regular grade levels
    enrollment_long.loc[
        enrollment_long["Grade Level"].isin(
            ["G1", "G2", "G3", "G4", "G5", "G6"]
        ),
        "Education Level"
    ] = "Elementary"

    enrollment_long.loc[
        enrollment_long["Grade Level"].isin(
            ["G7", "G8", "G9", "G10"]
        ),
        "Education Level"
    ] = "Junior High School"

    enrollment_long.loc[
        enrollment_long["Grade Level"].isin(
            ["G11", "G12"]
        ),
        "Education Level"
    ] = "Senior High School"

    # Initialize SHS track and strand fields
    enrollment_long["SHS Track"] = pd.NA
    enrollment_long["SHS Strand"] = pd.NA

    # Identify SHS records
    shs_mask = (
        enrollment_long["Education Level"]
        == "Senior High School"
    )

    # Extract SHS track
    enrollment_long.loc[shs_mask, "SHS Track"] = (
        enrollment_long.loc[
            shs_mask, "Enrollment Category"
        ]
        .str.extract(
            r"^G1[12]\s+(ACAD|TVL|SPORTS|ARTS)"
        )[0]
        .replace({
            "ACAD": "Academic",
            "TVL": "TVL",
            "SPORTS": "Sports",
            "ARTS": "Arts"
        })
    )

    # Extract academic strand
    academic_mask = (
        shs_mask
        & (enrollment_long["SHS Track"] == "Academic")
    )

    enrollment_long.loc[academic_mask, "SHS Strand"] = (
        enrollment_long.loc[
            academic_mask, "Enrollment Category"
        ]
        .str.extract(
            r"^G1[12]\s+ACAD\s*-?\s*(ABM|HUMSS|STEM|GAS|PBM)$"
        )[0]
    )

    return enrollment_long

# =============================================
# Validation
# =============================================

def validate_transformed_data(
    original_df: pd.DataFrame,
    school_enrollment: pd.DataFrame,
    enrollment_long: pd.DataFrame,
    enrollment_columns: list[str]
) -> None:
    """
    Validate the school-level and long-format datasets.
    """

    # Expected dimensions
    expected_long_rows = (
        len(original_df) * len(enrollment_columns)
    )

    # School-level dataset checks
    assert len(school_enrollment) == len(original_df)

    assert school_enrollment.shape[1] == (
        original_df.shape[1] + 3
    )

    # Long-format dataset checks
    assert len(enrollment_long) == expected_long_rows

    assert enrollment_long["Sex"].notna().all()

    assert enrollment_long["Grade Level"].notna().all()

    assert enrollment_long["Education Level"].notna().all()

    # Confirm all 29 categories are present
    assert (
        enrollment_long["Enrollment Category"].nunique()
        == 29
    )

    # Compare original and transformed enrollment totals
    original_total = (
        original_df[enrollment_columns].sum().sum()
    )

    school_total = (
        school_enrollment["Total Enrollment"].sum()
    )

    long_total = enrollment_long["Enrollment"].sum()

    assert original_total == school_total
    assert original_total == long_total

    # Check male and female totals
    original_male = original_df[
        [c for c in enrollment_columns if c.endswith(" Male")]
    ].sum().sum()

    original_female = original_df[
        [c for c in enrollment_columns if c.endswith(" Female")]
    ].sum().sum()

    long_sex_totals = (
        enrollment_long.groupby("Sex")["Enrollment"].sum()
    )

    assert long_sex_totals["Male"] == original_male
    assert long_sex_totals["Female"] == original_female

    print("All transformation validation checks passed!")
    print("--------------------------------------------")
    print(f"School-level shape: {school_enrollment.shape}")
    print(f"Long-format shape: {enrollment_long.shape}")
    print(f"Enrollment categories: {enrollment_long['Enrollment Category'].nunique()}")
    print(f"Male enrollment: {original_male:,}")
    print(f"Female enrollment: {original_female:,}")
    print(f"Total enrollment: {original_total:,}")

# =============================================
# Save Processed Datasets
# =============================================

def save_transformed_data(
    school_enrollment: pd.DataFrame,
    enrollment_long: pd.DataFrame
) -> None:
    """
    Save both analytical datasets as Parquet files.
    """

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    school_path = (
        OUTPUT_DIRECTORY / "school_enrollment.parquet"
    )

    long_path = (
        OUTPUT_DIRECTORY / "enrollment_long.parquet"
    )

    school_enrollment.to_parquet(
        school_path,
        index=False,
        engine="pyarrow"
    )

    enrollment_long.to_parquet(
        long_path,
        index=False,
        engine="pyarrow"
    )

    print("\nProcessed datasets saved successfully!")
    print(f"School-level: {school_path}")
    print(f"Long-format: {long_path}")

# =============================================
# Main Transformation Pipeline
# =============================================

def main():

    # Load cleaned dataset
    print("Loading cleaned dataset...")

    df = pd.read_parquet(INPUT_PATH)

    print(f"Loaded dataset: {df.shape}")

    # Identify columns
    enrollment_columns = get_enrollment_columns(df)

    metadata_columns = get_metadata_columns(
        df,
        enrollment_columns
    )

    print(f"Enrollment columns: {len(enrollment_columns)}")
    print(f"Metadata columns: {len(metadata_columns)}")

    # Create school-level dataset
    print("\nCreating school-level dataset...")

    school_enrollment = create_school_enrollment(
        df,
        enrollment_columns
    )

    # Create long-format dataset
    print("Creating long-format dataset...")

    enrollment_long = create_enrollment_long(
        df,
        enrollment_columns,
        metadata_columns
    )

    # Validate both datasets
    print("\nValidating transformed datasets...")

    validate_transformed_data(
        df,
        school_enrollment,
        enrollment_long,
        enrollment_columns
    )

    # Save outputs
    save_transformed_data(
        school_enrollment,
        enrollment_long
    )


if __name__ == "__main__":
    main()
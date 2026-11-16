
import pytest

from src.data.validate import (
    load_prepared_datasets,
    validate_education_totals,
    validate_enrollment_totals,
    validate_enrollment_values,
    validate_grade_totals,
    validate_long_records,
    validate_missing_values,
    validate_school_ids,
    validate_shs_totals,
    validate_structure,
    validate_zero_enrollment,
)


@pytest.fixture(scope="module")
def prepared_datasets():
    """Load the prepared datasets once for this test module."""
    return load_prepared_datasets()


def test_dataset_structure(prepared_datasets):
    cleaned, school, long = prepared_datasets
    validate_structure(cleaned, school, long)


def test_school_ids(prepared_datasets):
    cleaned, school, long = prepared_datasets
    validate_school_ids(cleaned, school, long)


def test_enrollment_totals(prepared_datasets):
    cleaned, school, long = prepared_datasets
    validate_enrollment_totals(cleaned, school, long)


def test_education_level_totals(prepared_datasets):
    cleaned, school, _ = prepared_datasets
    validate_education_totals(cleaned, school)


def test_grade_level_totals(prepared_datasets):
    _, _, long = prepared_datasets
    validate_grade_totals(long)


def test_shs_strand_and_track_totals(prepared_datasets):
    _, _, long = prepared_datasets
    validate_shs_totals(long)


def test_enrollment_values(prepared_datasets):
    cleaned, _, long = prepared_datasets
    validate_enrollment_values(cleaned, long)


def test_zero_enrollment_records(prepared_datasets):
    cleaned, school, _ = prepared_datasets
    validate_zero_enrollment(cleaned, school)


def test_long_format_records(prepared_datasets):
    cleaned, _, long = prepared_datasets
    validate_long_records(cleaned, long)


def test_missing_value_counts(prepared_datasets):
    cleaned, school, _ = prepared_datasets
    validate_missing_values(cleaned, school)

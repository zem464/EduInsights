# EduInsight Data Preparation Report

## 1. Introduction

### 1.1 Purpose

This report documents the data preparation process performed for the **EduInsight: Philippine Basic Education Enrollment Analytics Platform**. The purpose of this phase was to convert the original school-level enrollment dataset into clean, structured, and validated datasets suitable for exploratory data analysis, analytical processing, and interactive dashboard development.

The preparation process covered source data extraction, cleaning and standardization, dataset transformation, creation of derived analytical measures, and validation of the resulting datasets.

### 1.2 Scope

The data preparation process consisted of the following activities:

- **Data Extraction:** Loading the original Excel workbook and extracting school-level records from the designated worksheet.
- **Data Cleaning:** Standardizing missing-value representations and trimming unnecessary whitespace from text fields.
- **Data Transformation:** Producing school-level and long-format enrollment datasets while preserving the original school metadata and enrollment information.
- **Derived Measures:** Calculating enrollment totals by sex and education level, enrollment shares, male-female enrollment differences, and zero-enrollment indicators.
- **Data Validation:** Performing structural, numerical, and record-level checks, followed by automated testing using pytest and code-quality inspection using Ruff.

The prepared datasets serve as the foundation for subsequent analytical activities and dashboard development.

### 1.3 Dataset Coverage

The project uses the *School Level Data on Official Enrollment in All Grade Levels* dataset for School Year 2023–2024, with a reference date of January 31, 2024.

The source contains school-level enrollment records covering Kindergarten, Elementary, Junior High School, and Senior High School. Enrollment information is disaggregated by sex and includes grade-level and Senior High School strand or track categories.

The dataset contains 60,167 school records, 14 school metadata fields, and 58 enrollment fields, resulting in 72 original columns.

---

## 2. Source Dataset and Extraction

### 2.1 Source Dataset

The source dataset used in EduInsight is the Excel workbook:

`SY 2023-2024 School Level Data on Official Enrollment 13.xlsx`

The dataset is identified as *School Level Data on Official Enrollment in All Grade Levels* and was obtained from the Department of Education (DepEd) Learner Information System (LIS), as recorded in the project's dataset inventory.

The workbook contains three worksheets:

- `DB` – Main school-level enrollment dataset.
- `Zero Enrollment` – Summary of zero-enrollment records.
- `Sheet2` – Additional worksheet included in the source workbook.

The `DB` worksheet was selected as the primary source for the preparation pipeline because it contains the individual school records and their corresponding enrollment counts.

### 2.2 Source Dataset Structure

The `DB` worksheet contains 60,167 school records and 72 columns. Its column headers begin at Excel row 5, requiring the fifth row to be used as the header when loading the worksheet through pandas.

The 72 columns consist of:

| Field Group | Number of Columns | Description |
|---|---:|---|
| School Metadata | 14 | School identification and classification information, including BEIS School ID, school name, geographic attributes, and school characteristics. |
| Enrollment Data | 58 | Male and female enrollment counts across Kindergarten, Elementary, Junior High School, and Senior High School categories. |
| **Total** | **72** | **Complete source dataset structure.** |

The enrollment fields include Kindergarten, Grades 1–6, Elementary non-graded, Grades 7–10, Junior High School non-graded, and Senior High School grade-level strand and track categories.

### 2.3 Data Extraction Process

The source workbook was loaded using the pandas library through a reusable extraction module located at:

`src/data/load.py`

The module defines the project root directory using Python's `pathlib` library and constructs the source workbook path relative to the project directory. This approach avoids relying on a machine-specific absolute file path.

The extraction process uses `pandas.read_excel()` to read the `DB` worksheet and specifies `header=4` to correctly identify the column names from Excel row 5.

The loader also performs basic input validation by checking whether the source workbook exists and whether the extracted dataset matches the expected dimensions of 60,167 rows and 72 columns. If the workbook is missing or the extracted dimensions differ from the expected structure, the function raises an appropriate error.

The extracted dataset is returned as a pandas DataFrame for subsequent cleaning and transformation.

### 2.4 Extracted Dataset Output

The extraction process successfully loaded the expected school-level records from the source workbook.

| Validation Item | Expected Result | Actual Result |
|---|---:|---:|
| Source Worksheet | DB | DB |
| Header Row | 5 | 5 |
| Number of Records | 60,167 | 60,167 |
| Number of Columns | 72 | 72 |
| Extracted Dataset Shape | (60,167, 72) | (60,167, 72) |

The successful extraction established the source dataset used throughout the succeeding data preparation activities.

---

## 3. Data Cleaning and Standardization

### 3.1 Cleaning Objectives

The cleaning process aimed to improve the consistency of the extracted dataset while preserving its original structure and enrollment information.

The following operations were performed:

- Standardization of placeholder values in the `Street Address` column.
- Removal of leading and trailing whitespace from text fields.
- Preservation of the original school records, enrollment values, and metadata structure.

The cleaning process was implemented using pandas and NumPy in the project's data preparation workflow.

### 3.2 Missing-Value Standardization

Initial dataset inspection identified missing and placeholder-like values in the `Street Address` column. Some records contained representations such as `-`, `none`, `not applicable`, `-n/a`, `-none`, `n/a`, `na`, `null`, `nil`, and empty strings.

To standardize these entries, the values were stripped of surrounding whitespace, converted to lowercase for comparison, and replaced with `NaN` when they matched the predefined placeholder list.

This operation was limited to the `Street Address` column to avoid incorrectly interpreting legitimate values in other text fields.

Following standardization, the missing-value counts were:

| Column | Missing Values After Cleaning |
|---|---:|
| Street Address | 5,291 |
| Barangay | 70 |
| **Total Missing Cells** | **5,361** |

The increase in missing values for `Street Address` reflects the conversion of placeholder-like entries into a consistent missing-value representation. These values were not deleted, and their corresponding school records were retained.

### 3.3 Text Standardization

Leading and trailing whitespace was removed from values in text-based columns. This helped improve consistency in school names, geographic attributes, and classification fields without changing the intended content of the values.

The operation was applied to text columns only. Numeric enrollment fields and school identifiers were not modified by this procedure.

### 3.4 Data Integrity Checks After Cleaning

The cleaned dataset was checked to ensure that the cleaning operations did not introduce unintended changes.

| Validation Item | Result |
|---|---|
| Original Record Count | 60,167 |
| Cleaned Record Count | 60,167 |
| Original Column Count | 72 |
| Cleaned Column Count | 72 |
| Missing Enrollment Values | 0 |
| Negative Enrollment Values | 0 |
| Total Enrollment Before Cleaning | 27,081,292 |
| Total Enrollment After Cleaning | 27,081,292 |

The checks confirmed that the cleaning process preserved the original dataset dimensions and enrollment totals.

### 3.5 Cleaned Dataset Output

The cleaned dataset was saved in Apache Parquet format at:

`data/interim/school_records_cleaned.parquet`

Parquet was selected as the intermediate storage format because it supports efficient storage and retrieval of structured tabular data while preserving column data types.

The saved file was subsequently read back to verify that it could be loaded successfully and retained the expected dimensions.

---

## 4. Dataset Transformation

### 4.1 Transformation Objectives

The transformation process converted the cleaned school-level dataset into analytical structures suitable for different types of analysis.

Two datasets were generated:

1. **School-Level Dataset** – Retains one record per school and adds calculated enrollment measures.
2. **Long-Format Enrollment Dataset** – Converts the 58 enrollment columns into individual records organized by enrollment category and sex.

Both datasets retain the school metadata required for geographic, institutional, and enrollment analysis.

### 4.2 School-Level Dataset Transformation

The school-level dataset was created by preserving the original 72 columns and adding calculated enrollment fields.

The following measures were generated for each school:

- Male Enrollment
- Female Enrollment
- Total Enrollment

These measures were calculated by summing the corresponding male and female enrollment columns across all grade levels and Senior High School categories.

The resulting school-level dataset retained one record per school and expanded from 72 to 75 columns during the initial transformation.

During the succeeding derived-measure activity, eight additional analytical fields were added, resulting in a final total of 83 columns.

### 4.3 Long-Format Enrollment Transformation

The long-format dataset was generated by reshaping the 58 enrollment columns into rows using pandas' `melt()` operation.

Instead of representing each grade or strand and sex combination as a separate column, the transformed dataset stores enrollment information in individual records.

The transformation produced the following principal fields:

| Field | Description |
|---|---|
| BEIS School ID | Unique school identifier. |
| School Metadata | Original school-level attributes retained from the source dataset. |
| Enrollment Category | Grade-level or Senior High School enrollment category. |
| Enrollment | Enrollment count for the corresponding category and sex. |
| Sex | Male or Female. |
| Grade Level | Kindergarten, grade level, or non-graded category. |
| Education Level | Kindergarten, Elementary, Junior High School, or Senior High School. |
| SHS Track | Senior High School track, where applicable. |
| SHS Strand | Academic strand, where applicable. |
| School Total Enrollment | Total enrollment of the corresponding school. |
| Enrollment Share of School (%) | Percentage contribution of the record's enrollment to its school's total enrollment. |

The transformation also extracted the sex designation from the original enrollment column names and mapped grade-level categories to their corresponding education levels.

For Senior High School records, the transformation identified the Academic, TVL, Sports, and Arts tracks. Academic records were further classified into ABM, HUMSS, STEM, GAS, and PBM strands.

The resulting long-format dataset contains 3,489,686 records, equivalent to 60,167 schools multiplied by 58 enrollment fields.

### 4.4 Education-Level Classification

Enrollment categories were grouped into four broad education levels:

| Education Level | Included Categories |
|---|---|
| Kindergarten | Kindergarten |
| Elementary | Grades 1–6 and Elementary Non-Graded |
| Junior High School | Grades 7–10 and Junior High School Non-Graded |
| Senior High School | Grades 11–12, including their corresponding strands and tracks |

This classification provides a consistent basis for comparing enrollment across the major stages of basic education.

### 4.5 Transformation Validation

The transformation process included checks to ensure that:

- The school-level dataset retained the same number of school records as the cleaned source.
- The original metadata and enrollment columns were preserved.
- The long-format dataset contained exactly 58 enrollment records per school.
- Required classification fields, including sex, grade level, and education level, were populated.
- The total enrollment in the source, school-level, and long-format datasets reconciled.
- Male and female enrollment totals remained consistent after transformation.

All implemented transformation validation checks passed.

---

## 5. Derived Fields and Analytical Measures

### 5.1 Overview

Additional fields and measures were created to support the analytical requirements established during the project's planning phase.

These measures were added to the school-level dataset or the long-format dataset, depending on their intended analytical use.

### 5.2 School-Level Derived Measures

The following measures were added to the school-level dataset:

| Derived Field | Calculation or Rule |
|---|---|
| Male Enrollment | Sum of all male enrollment fields for each school. |
| Female Enrollment | Sum of all female enrollment fields for each school. |
| Total Enrollment | Sum of male and female enrollment for each school. |
| Kindergarten Enrollment | Sum of Kindergarten male and female enrollment. |
| Elementary Enrollment | Sum of Grades 1–6 and Elementary Non-Graded enrollment. |
| Junior High School Enrollment | Sum of Grades 7–10 and Junior High School Non-Graded enrollment. |
| Senior High School Enrollment | Sum of all Grade 11 and Grade 12 enrollment categories. |
| Male-Female Difference | Male Enrollment minus Female Enrollment. |
| Male Enrollment Share (%) | Male Enrollment divided by Total Enrollment, multiplied by 100. |
| Female Enrollment Share (%) | Female Enrollment divided by Total Enrollment, multiplied by 100. |
| Zero Enrollment Flag | Boolean indicator identifying schools with zero total enrollment. |

For schools with zero total enrollment, the male and female enrollment shares were assigned missing values because percentage calculations would involve division by zero.

### 5.3 Long-Format Derived Measures

Two additional measures were incorporated into the long-format dataset:

**School Total Enrollment**

Represents the total enrollment of the school associated with each long-format record. The value is mapped from the corresponding school-level enrollment total using the BEIS School ID.

**Enrollment Share of School (%)**

Measures the contribution of a particular enrollment category and sex to the school's total enrollment.

The calculation is:

`Enrollment Share of School (%) = (Enrollment / School Total Enrollment) × 100`

For schools with zero total enrollment, the percentage is undefined and is represented as a missing value.

### 5.4 Zero-Enrollment Identification

Schools with a total enrollment of zero were identified using the `Zero Enrollment Flag` field.

The resulting dataset retained 115 zero-enrollment school records. These records were not removed because they are relevant to the project's goal of examining enrollment distribution and identifying schools with no reported enrollment.

---

## 6. Data Validation

### 6.1 Validation Objectives

The validation process aimed to confirm that data cleaning, transformation, and derived-measure calculations did not introduce unintended record loss, inconsistencies, or numerical errors.

Validation was performed through reusable functions in `src/data/validate.py`, followed by automated testing using pytest.

### 6.2 Structural Validation

Structural checks verified the dimensions of the cleaned source and both prepared datasets.

| Dataset | Expected Dimensions | Actual Dimensions | Result |
|---|---:|---:|---|
| Cleaned Source | 60,167 × 72 | 60,167 × 72 | Passed |
| School-Level | 60,167 × 83 | 60,167 × 83 | Passed |
| Long-Format | 3,489,686 × 23 | 3,489,686 × 23 | Passed |

The school-level dataset was also checked to ensure that all original source columns were retained.

### 6.3 School Identifier and Record Validation

The BEIS School ID was used to verify school-level record uniqueness and consistency across the prepared datasets.

The validation confirmed that:

- All 60,167 school records had unique BEIS School IDs in the cleaned source.
- The school-level dataset contained no duplicate BEIS School IDs.
- The school identifiers represented in the source, school-level, and long-format datasets were consistent.
- Every school had exactly 58 records in the long-format dataset.
- The long-format dataset contained the expected 3,489,686 records.

The zero-enrollment records were independently recalculated from the cleaned source and compared with the corresponding flags in the school-level dataset. All 115 zero-enrollment records were retained and correctly identified.

### 6.4 Numerical Validation

Numerical validation compared enrollment totals across the source and prepared datasets.

The following checks were performed:

- Overall enrollment totals.
- Male and female enrollment totals.
- Reconciliation of male and female enrollment with total enrollment.
- Education-level enrollment totals.
- Grade-level enrollment totals.
- Senior High School strand and track totals.
- Negative, missing, and non-finite enrollment values.

The overall enrollment totals reconciled across all three datasets.

| Measure | Validated Total |
|---|---:|
| Total Enrollment | 27,081,292 |
| Male Enrollment | 13,854,090 |
| Female Enrollment | 13,227,202 |

The validation also confirmed that the sum of male and female enrollment equaled total enrollment and that the education-level, grade-level, and Senior High School breakdowns matched the established reference totals.

No negative, missing, or non-finite values were found in the enrollment fields of the cleaned source and long-format dataset.

### 6.5 Missing-Value Validation

Missing-value checks confirmed that the cleaning process preserved the expected missing-value counts in the relevant metadata fields.

| Field | Expected Missing Values | Actual Missing Values |
|---|---:|---:|
| Street Address | 5,291 | 5,291 |
| Barangay | 70 | 70 |

The school-level dataset also contained 115 missing values in each of the male and female enrollment share fields. These were expected because percentage shares are undefined for zero-enrollment schools.

Missing values in Senior High School track and strand fields were also retained where the classifications were not applicable to non-SHS records or non-Academic SHS categories.

### 6.6 Automated Testing with pytest

A separate automated test suite was created at:

`tests/test_data_pipeline.py`

The test suite contains 10 tests covering structural integrity, school identifiers, enrollment totals, education-level totals, grade-level totals, Senior High School classifications, enrollment values, zero-enrollment records, long-format record counts, and missing-value counts.

The test suite was executed using:

`python -m pytest -v`

**Test Results: 10 passed**

All 10 automated tests completed successfully.

### 6.7 Code Quality Inspection with Ruff

Ruff was used to inspect Python source files and the project notebook for code-quality issues, including import organization and line-length violations.

The identified issues were corrected, and the final Ruff check completed successfully using:

`ruff check .`

**Result: All checks passed.**

### 6.8 Overall Validation Result

All implemented structural, numerical, and record-level validation checks passed. The automated test suite also completed successfully, and the final code-quality inspection reported no remaining issues.

These results indicate that the prepared datasets retained the expected school records, enrollment information, and derived measures throughout the implemented preparation process.

---

## 7. Prepared Dataset Outputs

### 7.1 Output Files

The data preparation process generated three primary Parquet datasets.

| Dataset | File Path | Dimensions | Purpose |
|---|---|---:|---|
| Cleaned Source | `data/interim/school_records_cleaned.parquet` | 60,167 × 72 | Standardized source dataset used as input for transformation. |
| School-Level | `data/processed/school_enrollment.parquet` | 60,167 × 83 | School-level dataset containing original fields and derived enrollment measures. |
| Long-Format | `data/processed/enrollment_long.parquet` | 3,489,686 × 23 | Reshaped enrollment dataset supporting detailed analysis by school, grade, category, and sex. |

### 7.2 Output Format

The datasets were saved in Apache Parquet format using the PyArrow engine.

Parquet was selected to support efficient storage and retrieval of structured analytical datasets while retaining column data types.

The cleaned source dataset is stored in the `data/interim/` directory, while the final transformed datasets are stored in `data/processed/`.

### 7.3 Intended Analytical Use

The prepared datasets support different analytical requirements:

- **Cleaned Source:** Serves as the standardized reference dataset for transformation and verification.
- **School-Level Dataset:** Supports school counts, enrollment totals, geographic comparisons, sector analysis, and school-level exploration.
- **Long-Format Dataset:** Supports analysis by education level, grade level, Senior High School strand and track, and sex.

Together, these datasets provide the analytical foundation for the subsequent exploratory analysis and interactive dashboard development of EduInsight.

---

## 8. Data Preparation Limitations

Despite successful validation, several limitations and considerations remain relevant when interpreting the prepared datasets.

### 8.1 Single School Year Coverage

The source dataset covers School Year 2023–2024 only, with a reference date of January 31, 2024. Therefore, the prepared datasets support descriptive and comparative analysis within this reporting period but do not support historical enrollment trend analysis across multiple school years.

### 8.2 Missing Geographic Information

Some records contain missing values in the `Street Address` and `Barangay` fields. These values were standardized or retained as missing rather than being inferred or filled with unverified information.

Analyses that depend on these geographic fields may therefore have incomplete coverage.

### 8.3 Zero-Enrollment Records

A total of 115 schools have zero reported enrollment in the `DB` worksheet. These records were retained for transparency and analytical completeness.

A separate `Zero Enrollment` worksheet in the source workbook reports a different summary total from the school-level records in `DB`. The discrepancy was identified during the initial dataset audit but was not resolved during data preparation. The two worksheet totals should therefore not be treated as interchangeable without further investigation.

### 8.4 Interpretation of Derived Measures

Derived enrollment shares are undefined for schools with zero total enrollment. These values are represented as missing rather than being assigned an artificial percentage.

Similarly, high school-level enrollment values identified through statistical outlier detection should not automatically be interpreted as errors. They may represent large schools with legitimately higher enrollment.

### 8.5 Scope of Available Information

The source dataset contains reported enrollment counts and school metadata. It does not provide the additional information required to directly measure attendance, dropout rates, learner progression, enrollment rates using population denominators, or the causes of enrollment differences.

Consequently, analyses and visualizations based on these prepared datasets should remain within the scope of descriptive enrollment analysis.

---

## 9. Conclusion

The EduInsight data preparation phase successfully transformed the original School Year 2023–2024 school-level enrollment workbook into standardized and validated datasets suitable for analytical use.

The process produced a cleaned source dataset containing 60,167 school records and two prepared analytical datasets: a school-level dataset with 83 columns and a long-format dataset containing 3,489,686 records across 23 columns.

The resulting datasets preserve the original enrollment totals of 27,081,292 learners, including 13,854,090 male learners and 13,227,202 female learners. All 115 zero-enrollment school records were retained and correctly identified.

Structural, numerical, and record-level validation checks were completed successfully. The 10 automated pytest tests passed, and the final Ruff code-quality inspection reported no remaining issues.

With the preparation and validation activities completed, the resulting datasets are ready to serve as the foundation for the next phase of EduInsight: exploratory data analysis and the development of an interactive enrollment analytics dashboard.
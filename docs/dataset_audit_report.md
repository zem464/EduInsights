# EduInsight — Dataset Audit Report

## 1. Executive Summary

This report consolidates the dataset inventory, structural profile, data quality assessment, descriptive analysis, analytical opportunities, and identified limitations of the dataset selected for EduInsight.

The purpose of the audit is to assess the dataset's suitability for the development of an interactive Philippine basic education enrollment analytics platform and establish the requirements for data preparation and transformation.

The dataset contains school-level enrollment records for School Year 2023–2024, covering 60,167 schools and 58 male and female enrollment fields. The initial assessment identified missing geographic information, placeholder values in text fields, zero-enrollment records, and a discrepancy between the DB sheet and the separate Zero Enrollment worksheet.

Despite these considerations, the dataset provides sufficient information for descriptive and exploratory analysis of enrollment across geographic areas, school sectors, education levels, grade levels, and sex.

The findings of this audit will serve as the foundation for Phase 2: Data Preparation and Transformation.

## 2. Dataset Inventory

### 2.1 Dataset Information

| Attribute | Description |
|---|---|
| Dataset Name | School Level Data on Official Enrollment in All Grade Levels |
| Source | Department of Education (DepEd), Learner Information System (LIS) |
| File Name | SY 2023-2024 School Level Data on Official Enrollment 13.xlsx |
| File Format | Microsoft Excel Workbook (.xlsx) |
| File Size | Approximately 17.4 MB |
| School Year | 2023–2024 |
| Reference Date | January 31, 2024 |
| Acquisition Date | April 2025 |
| Primary Data Sheet | DB |
| Total School Records | 60,167 |
| Total Columns in DB | 72 |
| Enrollment Columns | 58 |

### 2.2 Workbook Sheet Inventory

The workbook contains three worksheets:

| Sheet Name | Description | Intended Use |
|---|---|---|
| DB | Contains school-level metadata and enrollment figures | Primary source for data preparation and analysis |
| Zero Enrollment | Contains regional and sector-level zero-enrollment summaries | Reference for validating zero-enrollment counts |
| Sheet2 | Additional worksheet in the source workbook | Requires inspection to determine whether it contains relevant information |

The DB sheet will serve as the primary source for the initial EduInsight data pipeline because it contains individual school records and their corresponding enrollment figures.

## 3. Structural Profile

### 3.1 Dataset Structure

The DB worksheet contains 60,167 rows and 72 columns.

| Structural Component | Count | Description |
|---|---:|---|
| School Records | 60,167 | Individual school-level records |
| School Metadata Columns | 14 | Geographic and school identification attributes |
| Enrollment Columns | 58 | Male and female enrollment counts |
| Total Columns | 72 | Combined metadata and enrollment fields |

The actual column headers are located on Excel row 5. When loading the worksheet using pandas, the correct header argument is `header=4`.

Each row represents one school record, identified through its BEIS School ID.

### 3.2 School Metadata

The first 14 columns contain school identification, geographic, and classification information.

These include attributes such as:

- BEIS School ID
- School Name
- Region
- Division
- District
- Province
- Municipality
- Barangay
- Street Address
- Legislative District
- Sector
- School Type
- School Classification
- Modified COC

These fields provide the dimensions needed for geographic and school-level exploration.

### 3.3 Enrollment Structure

The remaining 58 columns contain male and female enrollment counts across the following educational categories:

| Education Level | Enrollment Categories |
|---|---|
| Kindergarten | Kindergarten |
| Elementary | Grades 1–6 and Elementary Non-Graded |
| Junior High School | Grades 7–10 and Junior High School Non-Graded |
| Senior High School | Grades 11 and 12, including academic strands and specialized tracks |

Senior High School enrollment includes the following categories:

- Academic: ABM, HUMSS, STEM, GAS, and PBM
- Technical-Vocational-Livelihood (TVL)
- Sports
- Arts

Each enrollment category contains separate male and female fields.

### 3.4 Data Types

The initial structural inspection identified:

| Column Category | Observed Data Type | Assessment |
|---|---|---|
| School Identification and Geographic Fields | Text/Object | Requires standardization and validation |
| School Classification Fields | Text/Object | Requires category consistency checks |
| Enrollment Fields | Integer (int64) | Suitable for numerical aggregation |

All 58 enrollment columns were successfully identified and matched to their corresponding education categories. No unmatched enrollment columns or duplicate assignments were found during the profiling process.

## 4. Data Quality Assessment

### 4.1 Missing Values

The initial missing-value assessment identified the following:

| Column | Missing Values |
|---|---:|
| Street Address | 1,682 |
| Barangay | 70 |
| **Total Missing Cells** | **1,752** |

Street Address contains the highest number of missing values.

These counts represent missing cells, not necessarily unique school records, because a school may have missing information in more than one column.

### 4.2 Placeholder Values

The Street Address field also contains placeholder-like text values that may represent missing or unavailable information.

The identified values include:

| Placeholder Value | Count |
|---|---:|
| - | 2,375 |
| none | 475 |
| not applicable | 331 |
| -none | 214 |
| -n/a | 187 |
| na | 25 |
| n/a | 2 |
| **Total** | **3,609** |

Combining the 1,682 actual missing Street Address values with the 3,609 placeholder-like entries gives 5,291 entries requiring attention.

This represents approximately 8.80% of the 60,167 school records. However, placeholder values should not automatically be interpreted as confirmed missing addresses without considering their meaning.

No matching values from the predefined placeholder list were identified in the other 12 inspected text columns. This does not rule out other inconsistencies or invalid values.

### 4.3 Duplicate Records

| Check | Result |
|---|---:|
| Duplicate BEIS School IDs | 0 |
| Duplicate Complete Rows | 0 |

No duplicate BEIS School IDs or completely duplicated records were identified.

The BEIS School ID should still be validated during Phase 2 to ensure that it remains unique and complete after transformation.

### 4.4 Enrollment Data Validation

The 58 enrollment columns were assessed for numerical consistency.

| Validation Check | Result |
|---|---:|
| Enrollment Columns | 58 |
| Successfully Matched Columns | 58 |
| Unmatched Columns | 0 |
| Duplicate Assignments | 0 |
| Non-Numeric Enrollment Values After Conversion | 0 |
| Missing Enrollment Values After Conversion | 0 |
| Negative Enrollment Values | 0 |

The enrollment fields contain valid integer values based on the initial checks.

### 4.5 Zero-Enrollment Records

The DB sheet contains 115 school records with zero total enrollment.

Of these, seven are PSO schools, leaving 108 domestic zero-enrollment records.

**DB-derived zero-enrollment summary:**

| Sector | Zero-Enrollment Schools |
|---|---:|
| Public | 4 |
| Private | 103 |
| SUCsLUCs | 1 |
| **Domestic Total** | **108** |
| PSO | 7 |
| **Overall DB Total** | **115** |

However, the separate Zero Enrollment worksheet reports 206 zero-enrollment schools:

| Sector | Zero-Enrollment Schools |
|---|---:|
| Public | 11 |
| Private | 193 |
| SUCsLUCs / LUCs | 2 |
| **Total** | **206** |

The difference between the two sources is 98 records when comparing the worksheet total of 206 with the DB domestic total of 108.

The largest differences were observed in:

- Region IV-A: 43
- Region VII: 24
- NCR: 8
- Region III: 7

The reason for this discrepancy has not yet been established. It may reflect differences in coverage, inclusion criteria, or reporting methodology.

The DB sheet will be used for school-level zero-enrollment analysis because it contains individual school records. The discrepancy must remain documented and should not be resolved by arbitrarily modifying either source.

### 4.6 Potential Outliers

The initial statistical assessment identified high-enrollment outliers using the Interquartile Range (IQR) method.

| Statistical Measure | Value |
|---|---:|
| First Quartile (Q1) | 106 |
| Third Quartile (Q3) | 452 |
| Interquartile Range (IQR) | 346 |
| Lower Bound | -413 |
| Upper Bound | 971 |
| Potential High Outliers | 6,367 |
| Percentage of Schools | 10.58% |

Schools with total enrollment greater than 971 were classified as potential high outliers under this statistical rule.

These values should not automatically be treated as errors or removed. Large schools may legitimately have substantially higher enrollment than smaller schools.

The IQR results will be retained for exploratory analysis and further validation.

## 5. Descriptive Profile Summary

### 5.1 School Distribution

The dataset contains 60,167 school records across geographic areas and school categories.

**Regional Distribution:**

| Region | Number of Schools | Percentage |
|---|---:|---:|
| Region IV-A | 6,007 | 9.98% |
| Region III | 5,194 | 8.63% |
| PSO | 33 | 0.05% |

Region IV-A has the highest number of school records among the identified regions.

**Sector Distribution:**

| Sector | Number of Schools | Percentage |
|---|---:|---:|
| Public | 47,818 | 79.48% |
| Private | 12,113 | 20.13% |
| SUCsLUCs | 203 | 0.34% |
| PSO | 33 | 0.05% |

Public schools account for the largest share of school records.

**School Type Distribution:**

| School Type | Number of Schools | Percentage |
|---|---:|---:|
| School with no Annexes | 57,296 | 95.23% |
| Mother School | 2,015 | 3.35% |
| Annex or Extension School(s) | 843 | 1.40% |
| Mobile School(s)/Center(s) | 13 | 0.02% |

### 5.2 Enrollment Distribution

The overall recorded enrollment is 27,081,292.

**Enrollment by Sex:**

| Sex | Enrollment | Percentage |
|---|---:|---:|
| Male | 13,854,090 | 51.16% |
| Female | 13,227,202 | 48.84% |
| **Total** | **27,081,292** | **100%** |

Male enrollment exceeds female enrollment by 626,888.

**Enrollment by Education Level:**

| Education Level | Enrollment | Percentage |
|---|---:|---:|
| Kindergarten | 2,047,356 | 7.56% |
| Elementary | 13,154,595 | 48.58% |
| Junior High School | 7,749,265 | 28.62% |
| Senior High School | 4,130,076 | 15.25% |
| **Total** | **27,081,292** | **100%** |

Elementary accounts for the largest share of recorded enrollment.

**Enrollment by Sector:**

| Sector | Enrollment |
|---|---:|
| Public | 23,225,427 |
| Private | 3,731,936 |
| SUCsLUCs | 100,481 |
| PSO | 23,448 |
| **Total** | **27,081,292** |

Public schools account for the majority of recorded enrollment.

### 5.3 Statistical Summary

The statistical summary of total enrollment per school is:

| Statistical Measure | Value |
|---|---:|
| Count | 60,167 |
| Mean | 450.10 |
| Standard Deviation | 776.56 |
| Minimum | 0 |
| First Quartile (25%) | 106 |
| Median (50%) | 211 |
| Third Quartile (75%) | 452 |
| Maximum | 17,167 |

The mean enrollment is substantially higher than the median, indicating a right-skewed distribution. A relatively small number of schools have considerably higher enrollment than most schools.

The distribution supports the use of histograms and box plots for further exploration.

## 6. Analytical Opportunities

The dataset provides several opportunities for descriptive and exploratory analysis.

| Analytical Area | Opportunity | Potential Visualization |
|---|---|---|
| Geographic Analysis | Compare enrollment across regions, divisions, provinces, and municipalities | Horizontal Bar Chart, Map |
| School Distribution | Examine the number of schools across geographic areas and sectors | Horizontal Bar Chart |
| Education-Level Analysis | Compare enrollment across Kindergarten, Elementary, JHS, and SHS | Bar Chart, Donut Chart |
| Grade-Level Analysis | Identify enrollment differences across grade levels | Column Chart |
| Senior High School Analysis | Explore enrollment across academic strands and tracks | Horizontal Bar Chart |
| Demographic Analysis | Compare male and female enrollment | Donut Chart, 100% Stacked Bar Chart |
| School-Sector Analysis | Compare enrollment across Public, Private, SUCsLUCs, and PSO schools | Stacked Bar Chart |
| School-Level Analysis | Identify schools with the highest and zero recorded enrollment | Searchable Table |
| Enrollment Distribution | Examine school enrollment variation and potential outliers | Histogram, Box Plot |

These opportunities will guide the development of the National Overview, Geographic Exploration, Enrollment Analysis, and School Explorer sections of EduInsight.

## 7. Dataset Limitations

The following limitations must be considered during data preparation, analysis, and dashboard development.

### 7.1 Temporal Limitations

Only School Year 2023–2024 is available. The dataset cannot support year-over-year comparisons, historical enrollment trends, or enrollment growth analysis.

### 7.2 Population Limitations

The dataset does not include school-age population figures. Therefore, enrollment rates and the proportion of school-age children attending school cannot be calculated.

### 7.3 Individual Learner Limitations

The dataset contains aggregated school-level enrollment counts rather than individual learner records. Unique learner counts and individual learner tracking cannot be performed.

### 7.4 Attendance and Dropout Limitations

Attendance, dropout, and learner-progression information are not included. These indicators cannot be calculated from the available fields.

### 7.5 Geographic Limitations

Some geographic fields contain missing or placeholder values. Geographic drill-down and mapping require validation of location fields and their relationships.

### 7.6 Zero-Enrollment Discrepancy

The DB sheet and Zero Enrollment worksheet report different zero-enrollment totals. The discrepancy remains unresolved and must be documented in the dashboard's methodology where relevant.

### 7.7 Causal and Quality Limitations

The dataset supports descriptive comparisons but cannot establish why enrollment differs between regions, sectors, or schools. Enrollment counts alone also cannot determine educational quality or school performance.

## 8. Data Cleaning and Transformation Requirements

The audit findings establish the following requirements for Phase 2: Data Preparation and Transformation.

### 8.1 Data Loading and Extraction

- Load the source workbook using pandas.
- Use the DB worksheet as the primary school-level dataset.
- Specify `header=4` when reading the DB sheet because the actual headers are on Excel row 5.
- Inspect and document the structure of the remaining worksheets.
- Preserve the original source file as an unchanged raw dataset.

### 8.2 Column Standardization

- Standardize column names for easier processing and programming.
- Remove unnecessary leading or trailing whitespace from text values.
- Maintain a documented mapping between original column names and standardized names.
- Preserve BEIS School IDs as identifiers rather than treating them as numerical measures.

### 8.3 Missing Value Handling

- Identify actual missing values in geographic and school metadata fields.
- Standardize recognized placeholder values such as `-`, `none`, `not applicable`, `-n/a`, and `n/a`.
- Convert confirmed placeholders into consistent missing-value representations where appropriate.
- Preserve the distinction between unavailable, not applicable, and unknown information when the source meaning can be established.
- Do not invent missing geographic information.

### 8.4 Data Type Validation

- Ensure that enrollment fields use appropriate integer data types.
- Validate that enrollment values are non-negative.
- Ensure that school identification and categorical fields use appropriate text or categorical data types.
- Validate that BEIS School IDs are complete and unique.

### 8.5 Categorical Data Standardization

- Inspect unique values in geographic and school classification fields.
- Standardize inconsistent spacing, capitalization, and text formatting where appropriate.
- Preserve meaningful distinctions between school sectors, types, and classifications.
- Validate geographic naming conventions before grouping or mapping records.

### 8.6 Enrollment Transformation

- Generate total enrollment per school by summing the 58 enrollment fields.
- Calculate male and female enrollment totals separately.
- Group individual grade-level enrollment fields into Kindergarten, Elementary, JHS, and SHS categories.
- Group SHS enrollment fields into their corresponding academic strands and tracks.
- Create a consistent structure for geographic, sector, education-level, and demographic aggregation.
- Validate aggregated totals against the original enrollment fields.

### 8.7 Data Validation

- Recheck duplicate BEIS School IDs after transformation.
- Recheck missing and invalid values.
- Confirm that enrollment totals remain consistent before and after transformation.
- Validate zero-enrollment counts using the DB sheet.
- Retain the discrepancy with the Zero Enrollment worksheet as a documented source issue.
- Validate geographic relationships before implementing geographic drill-downs.
- Recalculate descriptive statistics to confirm that the transformed dataset produces consistent results.

### 8.8 Data Output and Storage

The preparation process should produce organized outputs for subsequent analysis and dashboard development.

| Data Layer | Purpose |
|---|---|
| Raw | Original source workbook preserved without modification |
| Interim | Extracted and standardized data during preparation |
| Processed | Validated and transformed dataset ready for analysis |
| Sample | Small representative dataset for testing and development |

Processed datasets should be reproducible from the raw source through documented Python scripts or notebooks.

## 9. Conclusion and Readiness for Data Preparation and Transformation

The initial audit indicates that the selected dataset is suitable for EduInsight's intended descriptive and exploratory analytics.

The dataset provides sufficient school-level metadata and enrollment measures to support geographic comparisons, education-level analysis, demographic comparisons, school-sector analysis, and school-level exploration.

However, data preparation is necessary to standardize metadata, handle placeholder values, validate geographic fields, calculate derived enrollment measures, and document unresolved source discrepancies.

The identified limitations must also be considered when developing dashboard indicators and interpreting results.

The findings and requirements in this report will serve as the reference for Data Preparation and Transformation, where the raw workbook will be converted into a consistent, validated, and analysis-ready dataset.
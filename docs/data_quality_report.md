# EduInsight — Data Quality Assessment Report

## 1. Overview

This report documents the data quality assessment performed on the DepEd School Level Data on Official Enrollment in All Grade Levels for School Year 2023–2024.

The assessment evaluates the completeness, consistency, validity, and reliability of the dataset before it is used for descriptive analysis and dashboard development.

**Dataset details:**
- **Source:** DepEd Learner Information System
- **School Year:** 2023–2024
- **Reference Date:** January 31, 2024
- **Primary Worksheet:** `DB`
- **Records Assessed:** 60,167 (to be confirmed against the structural profile)
- **Assessment Tool:** Python and Pandas

## 2. Assessment Scope

The following data quality dimensions were examined:

| Dimension | Assessment |
|---|---|
| Completeness | Identification of missing values in dataset columns |
| Consistency | Inspection of text values, category labels, and representations |
| Uniqueness | Detection of duplicate school identifiers and complete records |
| Validity | Examination of enrollment values for non-numeric, negative, or unexpected values |
| Enrollment Integrity | Identification and verification of schools with zero enrollment |
| Cross-Worksheet Consistency | Comparison of zero-enrollment counts between `DB` and `Zero Enrollment` |

## 3. Data Quality Assessment Results

### 3.1 Missing-Value Assessment

Missing values were identified using Pandas `isnull()`.

**Results:**

| Column | Missing Count |
|---|---:|
| Street Address | 1,682 |
| Barangay | 70 |
| **Total missing cells in these columns** | **1,752** |

No other columns were identified as having missing values in the initial assessment.

**Observation:**

Missing values are concentrated in the geographic information fields, particularly Street Address and Barangay. These missing entries may affect address-level or barangay-level geographic analysis.

**Recommended action:**

Retain missing values in the original dataset. Assess whether the affected records can still be used for regional, divisional, or municipal-level analysis.

### 3.2 Text-Value and Category Consistency Assessment

Text-based columns were examined using Pandas `value_counts(dropna=False)` to identify frequently occurring values, categorical distributions, and possible inconsistencies.

**Findings:**

**1. Geographic information**
- The Region column contains 15 distinct regional labels in the displayed results.
- Division and District contain different naming conventions and repeated generic names.
- Province values are consistently displayed in uppercase.
- Municipality and Legislative District use different naming formats.

**2. Street Address**

The Street Address column contains several placeholder-like text representations that may indicate unavailable or unreported address information.

| Placeholder Value | Count |
|---|---:|
| `-` | 2,375 |
| `none` | 475 |
| `not applicable` | 331 |
| `-none` | 214 |
| `-n/a` | 187 |
| `na` | 25 |
| `n/a` | 2 |
| **Total** | **3,609** |

In addition, 1,682 records contain actual missing values (`NaN`). Combining these with the identified placeholder-like entries gives 5,291 Street Address records requiring further attention, equivalent to approximately 8.80% of the dataset.

**Observation:**

The Street Address column contains multiple representations that may indicate missing or unavailable information. These values are not automatically recognized as missing by Pandas because they are stored as text. 

**Recommended action:**

- Investigate whether the identified placeholders have equivalent meanings.
- Treat confirmed placeholders as missing values only in a separate processed dataset.
- Preserve the original values in the raw dataset.
- Assess the effect of incomplete address information on geographic analysis.

**3. School Name**
- Similar school-name formats were observed, such as `San Isidro Elementary School` and `San Isidro ES`.
- These similarities do not establish that the records refer to the same school. BEIS School ID should be used as the school identifier rather than matching names alone.

**4. School classification**
- Sector contains four categories: Public, Private, SUCsLUCs, and PSO.
- School Subclassification contains nine categories.
- School Type contains four categories.
- Modified COC contains six categories.
- No category was automatically classified as invalid based solely on its frequency.

**Observation:**

The most notable text-value concern is the presence of placeholder-like entries in Street Address. Similar school-name formats and variations in geographic naming conventions also require consideration when preparing the dataset for analysis.

A systematic placeholder check was performed across all 13 text-based columns using a predefined list of common placeholder representations. Only the Street Address column contained matching placeholder-like entries, totaling 3,609. No matching placeholders were identified in the other 12 text columns. This check was limited to the predefined placeholder list and does not establish that all remaining categorical values are valid.

**Recommended action:**

- Preserve the original text values in the raw dataset.
- Further inspect placeholder-like address entries before treating them as missing.
- Use BEIS School ID to distinguish individual schools.
- Retain geographic and institutional categories unless inconsistencies are confirmed through an authoritative reference.
- Apply any necessary standardization only in a separate processed dataset.

### 3.3 Duplicate Assessment

Duplicate records were checked using the BEIS School ID and complete-row comparison.

**Results:**

| Duplicate Check | Duplicate Count |
|---|---:|
| BEIS School ID | 0 |
| Complete records | 0 |

**Observation:**

No duplicate BEIS School IDs or completely duplicated records were identified. This indicates that each school identifier appears only once in the assessed worksheet.

**Recommended action:**

Retain BEIS School ID as the primary school-level identifier for subsequent data processing.

### 3.4 Invalid-Value Assessment

The 58 enrollment columns were examined for data type consistency, missing values, and negative values.

**Results:**

| Validation Check | Result |
|---|---:|
| Enrollment columns | 58 |
| Numeric enrollment columns | 58 |
| Non-numeric enrollment columns | 0 |
| Missing enrollment values | 0 |
| Negative total enrollment records | 0 |

All enrollment columns were stored as `int64`. Numeric conversion also produced zero missing values, confirming that the enrollment fields contain numeric values.

**Observation:**

No non-numeric or negative enrollment values were identified. The enrollment fields passed the initial numerical validity checks.

**Recommended action:**

Retain the original enrollment values. Additional validation may be performed during descriptive profiling, including checking unusual enrollment distributions and unusually high school-level totals.

### 3.5 Zero-Enrollment Assessment

Zero-enrollment schools were identified by calculating the sum of all 58 enrollment fields for each school.

A school was classified as having zero enrollment when its total across all enrollment fields equaled zero.

**Results:**

| Assessment | Number of Schools |
|---|---:|
| Zero-enrollment records in `DB` | 115 |
| PSO records within `DB` zero-enrollment records | 7 |
| Domestic records in `DB` after excluding PSO | 108 |
| Records reported in `Zero Enrollment` worksheet | 206 |
| Difference in domestic counts | 98 |

**Regional and Sector Discrepancies:**

The comparison between the two worksheets revealed differences in the reported zero-enrollment counts.

The largest differences were observed in:

| Region | Sector | DB | Zero Enrollment Worksheet | Difference (DB − Worksheet) |
|---|---|---:|---:|---:|
| Region IV-A | Private | 12 | 55 | -43 |
| Region VII | Private | 2 | 26 | -24 |
| NCR | Private | 83 | 91 | -8 |
| Region III | Private | 3 | 10 | -7 |

Seven records in `DB` were classified under both Region and Sector as PSO. These records appear to represent Philippine schools located overseas. The summary worksheet does not provide a separate PSO category.

**Observation:**

The independently calculated zero-enrollment count from `DB` does not agree with the count reported in the `Zero Enrollment` worksheet. The discrepancy remains unresolved.

The enrollment fields in `DB` passed the numerical validation checks, but the reason for the difference between the worksheets has not yet been established.

**Recommended action:**

- Preserve both worksheets in their original form.
- Investigate the criteria used to generate the `Zero Enrollment` summary.
- Verify whether both worksheets use the same definition and coverage of zero enrollment.
- Do not automatically modify or remove records to force the counts to match.

## 4. Summary of Data Quality Findings

| Assessment Area | Result | Status |
|---|---|---|
| Missing values | Missing Street Address and Barangay entries | Identified |
| Text-value consistency | Pending inspection | Pending |
| Duplicate records | No duplicate IDs or complete rows | Passed |
| Enrollment validity | All 58 fields numeric; no missing or negative values | Passed initial checks |
| Zero-enrollment records | 115 identified in `DB` | Verified calculation |
| Cross-worksheet consistency | 98-record domestic discrepancy | Requires investigation |

## 5. Outstanding Issues and Limitations

The following issues require further investigation:

1. The reason for the discrepancy between the 115 zero-enrollment records in `DB` and the 206 records reported in the summary worksheet.
2. The criteria used to classify a school as having zero enrollment in the source workbook.
3. The treatment and geographic classification of PSO records.
4. The effect of missing Street Address and Barangay values on geographic analysis.
5. Any inconsistent or unexpected categorical values identified during the remaining text-value assessment.

## 6. Data Handling and Recommendations

Based on the initial assessment, the following data handling practices are recommended:

- Preserve the original workbook as an unchanged raw data source.
- Perform cleaning and standardization on separate working copies.
- Retain school identifiers to support record traceability.
- Do not automatically replace missing geographic values.
- Investigate unresolved discrepancies before using affected figures in published visualizations.
- Document all cleaning, transformation, and exclusion rules in the data processing pipeline.

## 7. Conclusion

The initial data quality assessment identified no duplicate school identifiers, duplicate complete records, missing enrollment values, non-numeric enrollment fields, or negative total enrollment records.

However, missing geographic information and an unresolved discrepancy between the school-level `DB` worksheet and the `Zero Enrollment` summary worksheet were identified.

The dataset is suitable for continued exploratory assessment, subject to documenting these findings and investigating the unresolved discrepancies before presenting affected figures as validated results.
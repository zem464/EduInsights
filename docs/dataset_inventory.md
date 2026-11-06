# EduInsight — Dataset Inventory

## 1. Dataset Information

| Attribute                         | Description                                                  |
| --------------------------------- | ------------------------------------------------------------ |
| Dataset name                      | School Level Data on Official Enrollment in All Grade Levels |
| Original filename                 | SY 2023-2024 School Level Data on Official Enrollment 13     |
| File format                       | xlsx                                                         |
| Data source                       | DepEd Learner Information System                             |
| School year                       | 2023-2024                                                    |
| Reference date / reporting period | January 31, 2024                                             |
| Date acquired                     | April 2025                                                   |
| File size                         | 17.4 MB                                                      |
| Intended use                      | Portfolio Project                                            |

## 2. Worksheet Inventory

| Worksheet | Purpose | Header Location | Record Structure |
|---|---|---|---|
| DB | Main school-level enrollment dataset | Row 5 | One row per school, containing school identifiers, geographic details, classifications, and enrollment counts by grade level and sex. |
| Zero Enrollment | Summary of schools without enrollment | Row 5 | Aggregated counts of schools without enrollment, grouped by region and school sector. |
| Sheet2 | Contains school-status or classification entries; exact purpose requires further inspection. | Not yet confirmed | Appears to contain a list of school-status or classification values rather than individual school records. |

## 3. Dataset Coverage

| Coverage Attribute | Observation |
|---|---|
| Geographic coverage | Includes Region, Division, District, Province, Municipality, Legislative District, and Barangay. |
| School coverage | Includes BEIS School ID, School Name, School Subclassification, and School Type. |
| Education levels | Kindergarten, Elementary, Junior High School, and Senior High School. |
| School sectors | Includes Sector classifications recorded in the dataset. |
| Sex categories | Male and Female. |
| Reporting period | January 31, 2024. |
| Dataset size | 60,167 school records and 72 columns. |
| Column composition | 14 school metadata columns and 58 enrollment columns. |                                       

## 4. Initial Observations

- The DB worksheet contains introductory information before the actual column headers.
- Enrollment fields are organized by education level, grade, and sex.
- The Zero Enrollment worksheet provides aggregated counts by region and school sector.
- The Sheet2 worksheet contains entries related to school status or enrollment participation.
- The DB worksheet includes a Modified COC field whose meaning requires clarification.

## 5. Known Limitations

- Only SY 2023–2024 is available
- No individual learner records
- Data reflects a specific reporting date
- Some school records have incomplete address information, which may limit detailed geographic analysis.

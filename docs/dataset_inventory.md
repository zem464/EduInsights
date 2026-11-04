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

| Worksheet | Purpose                       | Header Location | Record Structure                                                                                                  |
| --------- | ----------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------- |
| DB        | Shows all the enrollment data | Row 5           | One row per school with BEIS school identifiers, location details, school classifications, and enrollment counts. |
|           |                               |                 |                                                                                                                   |
|           |                               |                 |                                                                                                                   |

## 3. Dataset Coverage

| Coverage Attribute  | Observation                                                                |
| ------------------- | -------------------------------------------------------------------------- |
| Geographic coverage | Involves Regions, Divisions, Districts, Province, Municipal, and Barangays |
| School coverage     | Includes BEIS, School subclassification, and School type                   |
| Education levels    | Kindergarten, Elementary, Junior High School, Senior High School           |
| School sectors      | Public / Private                                                           |
| Sex categories      | Male / Female                                                              |
| Reporting period    | January 31, 2024                                                           |

## 4. Initial Observations

- There are introductory header in A1:A3 hence, headers starts at row 5. However, the grade level and sex classification are located at row 3 and row 4 from column O onwards.
- Columns from column O onwards are merged in row 3 and grouped by grade level.
- Zero values are used to indicate no enrollment.

## 5. Known Limitations

- Only SY 2023–2024 is available
- No individual learner records
- Data reflects a specific reporting date

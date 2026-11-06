# EduInsight — Structural Profile

## 1. Workbook Overview

- Original filename: SY 2023-2024 School Level Data on Official Enrollment 13
- File format: xlsx
- Number of worksheets: 3
- Worksheet names: 'DB', 'Zero Enrollment', 'Sheet2'

## 2. Worksheet Structure

| Worksheet | Header Location | Purpose |
|---|---|---|
| DB | Row 5 | Contains the main dataset. |
| Zero Enrollment | Row 5 | Contains the data for schools wihtout enrollment |
| Sheet2 | NULL | Only contains school classifications. |

## 3. Main Dataset Dimensions

- Total records: 60,167
- Total columns: 72
- Header row: 5

## 4. Column Organization

| Category | Number of Columns | Column(s) name |
|---|---:|---|
| School identifiers | 1 | BEIS School ID |
| Geographic information | 8 | Region, Division, District, Street Address, Province, Municipality, Legislative District, Barangay |
| School classification | 5 | School Name, Sector, School Subclassification, School Type, Modified COC |
| Enrollment measures | 57 | Male/Female from Kindergarten to G12 (ABM, HUMSS, STEM, GAS, PBM, TVL, Sports, Arts & Design) |

## 5. Data Type Distribution

| Data Type | Number of Columns | Percentage |
|---|---:|---:|
| object | 0 | 0 |
| int64 | 59 | 81.94 |
| str | 13 | 18.06 |

## 6. Structural Observations

- The worksheets includes two working sheets with one worksheet serving as a classification list.
- The main worksheets has introductory rows (1-4) including the data title and period of the dataset acquisition.
- Each row represents different schools.
- Enrollment data are subclassified by sex and grouped by grade level. 
- Some school address fields contain the value "NONE", which may need to be distinguished from genuinely missing values.
- Data type distribution consists of 59 integer columns and 13 string columns. The integer columns include 58 enrollment measures and one school identifier.
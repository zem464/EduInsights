# EduInsight — Analytics Requirements

## 1. Purpose

EduInsight is an interactive Philippine basic education enrollment analytics platform designed for the general public, students, and researchers.

Its primary purpose is to provide an accessible way to explore, compare, and analyze school-level enrollment data across geographic areas, school sectors, education levels, grade levels, and demographic categories.

The platform will use the School Level Data on Official Enrollment in All Grade Levels for School Year 2023–2024, with a reference date of January 31, 2024.

EduInsight will focus on descriptive and exploratory analytics through interactive visualizations, filtering capabilities, geographic comparisons, and school-level exploration. It aims to make enrollment data easier to understand and investigate without requiring advanced data analytics knowledge.

## 2. Analytical Components

### 2.1 Dimensions

Dimensions are categorical attributes used to group, filter, and organize enrollment data.

| Dimension Category | Fields | Description |
|---|---|---|
| Geographic Dimensions | Region, Division, Street, Province, Municipality, Legislative District, Barangay | Identify the geographic location of schools |
| School Dimensions | School Name, BEIS School ID, Sector, School Classification, School Type, Modified COC | Identify and categorize individual schools |
| Enrollment Dimensions | Education Level, Grade Level, SHS Strand, SHS Track | Categorize enrollment by educational level and program |
| Demographic Dimensions | Sex | Categorize enrollment by male and female learners |

### 2.2 Measures

Measures are numerical values used to quantify and analyze enrollment and school records.

| Measure Category | Measures | Description |
|---|---|---|
| Core Measures | Total Enrollment, Male Enrollment, Female Enrollment, Number of Schools | Direct numerical values obtained or calculated from the dataset |
| Derived Measures | Average Enrollment per School, Enrollment Share, Male-Female Enrollment Difference, Zero-Enrollment Schools | Values calculated from existing measures to support further analysis |

**Derived Measure Calculations:**

| Derived Measure | Calculation |
|---|---|
| Average Enrollment per School | Total Enrollment ÷ Number of Schools |
| Enrollment Share | Category Enrollment ÷ Total Enrollment × 100 |
| Male Enrollment Share | Male Enrollment ÷ Total Enrollment × 100 |
| Female Enrollment Share | Female Enrollment ÷ Total Enrollment × 100 |
| Male-Female Enrollment Difference | Male Enrollment − Female Enrollment |
| Zero-Enrollment Schools | Count of schools where Total Enrollment = 0 |

### 2.3 Key Performance Indicators (KPIs)

KPIs are summary indicators used to present important enrollment information.

| KPI | Description |
|---|---|
| Total Enrollment | Combined male and female enrollment across the selected records |
| Total Schools | Number of school records represented in the dataset |
| Male Enrollment Share | Percentage of recorded enrollment attributed to males |
| Female Enrollment Share | Percentage of recorded enrollment attributed to females |
| Zero-Enrollment Schools | Number of schools with zero recorded enrollment |

Additional indicators, such as average enrollment per school and enrollment distribution by education level, may be presented in detailed analytical sections.

All applicable KPIs should update according to the user's selected dashboard filters.

## 3. Analytical Questions

The following analytical questions will guide the dashboard's visualizations, filters, and interactions. They are intended to support public exploration and descriptive research.

### 3.1 Geographic Analysis

| ID | Analytical Question | Required Dimensions / Measures |
|---|---|---|
| AQ01 | Which regions have the highest and lowest recorded enrollment? | Region, Total Enrollment |
| AQ02 | Which divisions have the highest and lowest recorded enrollment? | Division, Total Enrollment |
| AQ03 | Which provinces and municipalities have the highest number of schools? | Province, Municipality, Number of Schools |
| AQ04 | How is enrollment distributed across geographic areas? | Region, Division, Province, Municipality, Total Enrollment |

### 3.2 Education-Level Analysis

| ID | Analytical Question | Required Dimensions / Measures |
|---|---|---|
| AQ05 | How is enrollment distributed across Kindergarten, Elementary, Junior High School, and Senior High School? | Education Level, Total Enrollment |
| AQ06 | Which grade levels have the highest and lowest enrollment? | Grade Level, Total Enrollment |
| AQ07 | How is Senior High School enrollment distributed across academic strands and tracks? | SHS Strand/Track, Grade Level, Total Enrollment |

### 3.3 Demographic Analysis

| ID | Analytical Question | Required Dimensions / Measures |
|---|---|---|
| AQ08 | What is the distribution of male and female enrollment? | Sex, Enrollment |
| AQ09 | How does the male-to-female enrollment distribution vary across regions? | Region, Sex, Enrollment |
| AQ10 | Which education levels have the highest male and female enrollment? | Education Level, Sex, Enrollment |

### 3.4 School-Sector Analysis

| ID | Analytical Question | Required Dimensions / Measures |
|---|---|---|
| AQ11 | How does enrollment differ among Public, Private, SUCsLUCs, and PSO schools? | Sector, Total Enrollment |
| AQ12 | Which sectors account for the largest share of school records? | Sector, Number of Schools |
| AQ13 | How does average enrollment per school vary by sector? | Sector, Total Enrollment, Number of Schools |
| AQ14 | Which school types and classifications account for the most school records? | School Type, School Classification, Number of Schools |

### 3.5 School-Level Analysis

| ID | Analytical Question | Required Dimensions / Measures |
|---|---|---|
| AQ15 | Which schools have the highest recorded enrollment? | School Name, BEIS School ID, Region, Total Enrollment |
| AQ16 | Which schools have zero recorded enrollment? | School Name, BEIS School ID, Total Enrollment |
| AQ17 | Which schools have unusually high enrollment compared with other schools? | School Name, BEIS School ID, Sector, Total Enrollment |
| AQ18 | How does enrollment vary among schools within the same region or sector? | Region, Sector, School Enrollment |

**Note:** AQ17 focuses on unusually high enrollment because the IQR assessment identified potential high outliers. These records should be investigated rather than automatically treated as errors. Unusually low enrollment should only be included once a meaningful threshold has been established.

## 4. Dashboard Requirements

### 4.1 Main KPI Cards

The National Overview dashboard should display the following primary indicators:

| KPI | Purpose |
|---|---|
| Total Enrollment | Present the overall recorded enrollment |
| Total Schools | Show the number of school records represented |
| Male Enrollment Share | Present the proportion of male enrollment |
| Female Enrollment Share | Present the proportion of female enrollment |

Additional indicators for detailed analysis may include:

- Average enrollment per school
- Zero-enrollment school count
- Kindergarten to SHS enrollment distribution
- Grade-level enrollment
- SHS strand and track enrollment
- Male and female enrollment comparisons
- Public, Private, SUCsLUCs, and PSO enrollment comparisons

KPI values should update dynamically according to the selected dashboard filters.

### 4.2 Dashboard Filters

Filters allow users to narrow the dataset and explore enrollment from different perspectives.

| Filter | Purpose |
|---|---|
| Region | View enrollment and school records within a selected region |
| Division | Narrow results to a specific schools division |
| Province | Filter records by province |
| Municipality | Narrow results to a municipality or city |
| Sector | Compare Public, Private, SUCsLUCs, and PSO schools |
| School Type | Compare school organizational arrangements |
| School Classification | Compare institutional classifications |
| Education Level | Filter Kindergarten, Elementary, JHS, or SHS |
| Grade Level / Strand | Examine a specific grade level or SHS program |
| Sex | Compare male and female enrollment |

**Filter Behavior:**
- Applicable KPI cards and visualizations should update when a filter is selected.
- Geographic filters should narrow available geographic selections when source relationships support the filtering.
- Users should be able to clear filters and return to the overall dataset view.
- Filters should be relevant to the current dashboard section instead of displaying every available filter on every page.
- PSO records should remain accessible even though they do not belong to the domestic geographic hierarchy.

### 4.3 Required Visualizations

| Dashboard Section | Visualization | Purpose |
|---|---|---|
| KPI Overview | KPI Cards | Highlight important enrollment indicators |
| Enrollment by Region | Horizontal Bar Chart | Compare regional enrollment |
| Schools by Region | Horizontal Bar Chart | Compare school counts across regions |
| Enrollment by Education Level | Bar or Donut Chart | Show enrollment distribution across education levels |
| Enrollment by Sex | Donut Chart or 100% Stacked Bar Chart | Compare male and female enrollment shares |
| Enrollment by Grade Level | Column Chart | Compare enrollment across grade levels |
| SHS Strand Distribution | Horizontal Bar Chart | Compare enrollment across SHS academic strands and tracks |
| Enrollment by Sector | Stacked Bar or Donut Chart | Compare enrollment distribution among school sectors |
| Geographic Distribution | Map | Show geographic enrollment patterns, if reliable geographic data is available |
| School-Level Enrollment | Searchable and Sortable Table | Find and examine individual school records |
| Enrollment Distribution | Histogram / Box Plot | Examine school enrollment variation and potential outliers |

Visualizations should include meaningful titles, labels, legends, and tooltips. Enrollment values should use consistent formatting, and percentage charts should clearly identify their denominators.

### 4.4 Geographic Drill-Down

The dashboard should support geographic exploration through the following proposed structure:

| Level | Example / Description |
|---|---|
| Region | Region IV-A |
| Division | Rizal |
| Province / Municipality | Geographic filtering based on available records |
| School | School Name and BEIS School ID |

**Proposed Navigation:**

Region → Division → Province / Municipality → School

**Implementation Considerations:**
- Users should be able to explore enrollment from broader geographic areas to individual school records.
- Geographic selections should update applicable charts and summary indicators.
- Parent-child relationships must be validated using actual source records before implementing cascading filters.
- Province and municipality relationships should account for cities and special geographic entries in the dataset.
- PSO records should be handled separately from domestic geographic drill-downs.

## 5. Data Limitations and Unsupported Questions

The platform must clearly communicate the limitations of the available dataset to prevent unsupported conclusions.

| Question | Why It Cannot Be Answered |
|---|---|
| How much has enrollment grown or declined compared with previous school years? | Only School Year 2023–2024 is available. |
| What is the enrollment rate of school-age children? | No corresponding school-age population denominator is provided. |
| How many unique learners are enrolled nationwide? | The dataset contains aggregated school-level counts, not individual learner identifiers. |
| What is the dropout rate? | No dropout or learner-progression information is available. |
| What is the attendance rate? | Attendance information is not included. |
| Why do some schools have zero enrollment? | The dataset does not explain the reason for each zero-enrollment record. |
| What causes enrollment differences between regions? | The dataset supports descriptive comparisons but does not establish causal relationships. |
| Which schools provide better-quality education? | Enrollment figures alone are not sufficient measures of educational quality. |

**Additional Data Considerations:**
- The dataset represents a snapshot with a reference date of January 31, 2024, not live or real-time enrollment information.
- Enrollment counts should be interpreted as recorded school-level aggregates, not necessarily unique individual learners.
- Statistical outliers should be treated as records for further investigation, not automatically classified as errors.
- Geographic comparisons depend on the consistency and completeness of location fields.
- The DB sheet and the separate Zero Enrollment worksheet have different zero-enrollment totals. School-level zero-enrollment analysis should use the DB sheet's school records and document the discrepancy rather than silently combining the two sources.
- Missing values and placeholder text values should be distinguished during data processing.

## 6. Initial Dashboard Scope

The initial development of EduInsight will focus on descriptive and exploratory analytics using the available School Year 2023–2024 dataset.

The platform will consist of four main dashboard sections:

| Dashboard Section | Description |
|---|---|
| National Overview | Presents national enrollment KPIs, education-level distribution, sex distribution, and regional comparisons. |
| Geographic Exploration | Enables comparisons of enrollment and school counts across regions, divisions, provinces, and municipalities. |
| Enrollment Analysis | Provides detailed exploration of enrollment by education level, grade, SHS strand or track, sex, and school sector. |
| School Explorer | Provides a searchable and filterable table of individual school records and their enrollment figures. |

**Initial Development Priorities:**
1. Present key enrollment indicators through a National Overview.
2. Enable geographic comparisons of enrollment and school counts.
3. Provide enrollment breakdowns by education level, grade, SHS strand or track, sex, and sector.
4. Allow users to search, filter, and examine individual school records.
5. Provide interactive filters and visualizations for exploratory analysis.
6. Display the dataset source, school year, reference date, and data limitations.

**Out of Scope:**
- Predictive enrollment modeling
- Causal analysis
- Historical trend analysis
- Enrollment-rate calculations
- Dropout and attendance analysis
- Live or real-time DepEd data integration
- Automated recommendations for education resource allocation

These features require additional datasets, historical records, or validated information beyond the current dataset.

The initial version of EduInsight will prioritize accessibility, transparency, and interactive exploration, allowing users to investigate Philippine basic education enrollment patterns while understanding the limitations of the available data.
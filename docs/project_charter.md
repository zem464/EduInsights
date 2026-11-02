# EduInsight — Project Charter

**Project Title:** EduInsight: Philippine Basic Education Enrollment Analytics Platform  
**Project Type:** Independent Data Analytics and Business Intelligence Portfolio Project  
**Project Status:** Planning and Requirements Definition  
**Version:** 1.0  
**Prepared By:** Project Developer

---

## 1. Project Overview

EduInsight is an independent data analytics project designed to organize, process, analyze, and visualize Philippine basic education enrollment data.

The project aims to demonstrate how structured data workflows, data quality assessment, exploratory data analysis, and interactive dashboards can transform raw enrollment records into meaningful information for educational planning and decision-making.

The platform will provide an interactive dashboard that allows users to explore enrollment patterns through relevant indicators, filters, and visualizations.

The project will use available and authorized enrollment datasets, with a reproducible file-based data processing workflow.

## 2. Problem Statement

Educational enrollment data can provide valuable insights into student population trends, school-level distribution, and changes in enrollment across grade levels and school years.

However, raw datasets may require considerable preparation before they can be used effectively for analysis. Inconsistent formats, missing values, unclear field definitions, and fragmented data structures can make it difficult to interpret and communicate findings.

Without a structured data workflow and accessible visualizations, users may spend additional time preparing data and identifying patterns that could otherwise support educational planning.

EduInsight addresses this challenge by establishing a structured data pipeline, documenting the dataset through a data dictionary, assessing data quality, and presenting relevant enrollment indicators through an interactive dashboard.

## 3. Project Objectives

The project has five primary objectives:

1. **Document the Data Workflow** — Develop a workflow map illustrating how enrollment data is acquired, validated, transformed, stored, analyzed, and presented.
2. **Develop a Data Dictionary** — Identify and document dataset fields, descriptions, data types, formats, and relevant constraints.
3. **Establish a Data Processing Pipeline** — Build a reproducible Python-based workflow for data ingestion, cleaning, validation, and transformation.
4. **Conduct Exploratory Data Analysis** — Examine enrollment distributions, trends, comparisons, and other relevant patterns in the available dataset.
5. **Develop an Interactive Dashboard** — Create a dashboard that presents enrollment KPIs, visualizations, and filters to support data exploration and educational planning.

## 4. Intended Users and Stakeholders

| Stakeholder | Role or Interest |
|---|---|
| DepEd personnel | Potential users of enrollment summaries and visualizations |
| School administrators | May use enrollment trends to understand student population patterns |
| Education planners | May use aggregated enrollment indicators to support planning |
| Project developer | Responsible for designing, implementing, testing, and documenting EduInsight |
| Academic reviewers / portfolio evaluators | Assess the project's technical implementation and analytical quality |

The dashboard is intended as an analytical and informational tool. It is not intended to replace official DepEd reporting systems or institutional decision-making processes.

## 5. Project Scope

### 5.1 In Scope

The project includes:

- Inspection and profiling of available enrollment datasets.
- Documentation of dataset structure and field definitions.
- Creation of a data workflow map.
- Data cleaning and standardization.
- Handling and documentation of missing, duplicate, and inconsistent records.
- Data validation and quality checks.
- Exploratory data analysis using Python.
- Calculation of relevant enrollment indicators and KPIs.
- Development of interactive charts and dashboard filters.
- Local or manually initiated dataset refresh through authorized file ingestion.
- Technical documentation and project testing.
- Version control using Git and GitHub.

### 5.2 Out of Scope

The following are excluded from the initial project:

- Direct integration with the production DepEd BEIS system.
- Automated access to restricted government databases.
- Real-time enrollment monitoring.
- Modification of official DepEd records.
- Student-level profiling or individual student tracking.
- Predictive analytics or machine learning unless justified by the dataset and project requirements.
- Production deployment for official institutional use.
- Replacement of existing DepEd information systems.

These features may be considered in future versions if appropriate access, requirements, and resources become available.

## 6. Major Project Deliverables

| Deliverable | Description |
|---|---|
| Project Charter | Defines the project's purpose, objectives, scope, and constraints |
| Data Workflow Map | Visual representation of the enrollment data processing workflow |
| Data Dictionary | Documentation of dataset fields and their definitions |
| Data Quality Report | Summary of missing values, duplicates, inconsistencies, and validation results |
| Cleaned Dataset | Processed and standardized analytical dataset |
| Exploratory Data Analysis | Analysis of enrollment distributions, trends, and patterns |
| Interactive Dashboard | Dashboard containing enrollment KPIs, charts, and filters |
| Technical Documentation | Setup instructions, methodology, architecture, and usage guide |
| Test Results | Evidence of data validation and application testing |

## 7. Proposed Technology Stack

| Technology | Intended Use |
|---|---|
| Python | Main programming language |
| Pandas | Data cleaning, manipulation, and analysis |
| DuckDB | Analytical querying and data storage |
| Plotly | Interactive data visualizations |
| Dash | Interactive dashboard development |
| Dash Bootstrap Components | Dashboard layout and styling |
| Openpyxl | Excel file ingestion |
| Pytest | Automated testing |
| Ruff | Code quality and linting |
| Git and GitHub | Version control and project collaboration or portfolio publishing |
| Visual Studio Code | Development environment |

The technology stack may be adjusted based on the actual dataset structure and implementation requirements.

## 8. Project Assumptions

The project is based on the following assumptions:

1. An enrollment dataset will be available for analysis.
2. The dataset can be used for independent educational and portfolio purposes.
3. The available data contains sufficient fields to support meaningful enrollment analysis.
4. The dataset's structure, coverage, and definitions will be verified during the dataset audit.
5. Data processing will be performed locally unless another authorized environment is established.
6. Any sensitive or restricted information will be excluded, anonymized, or otherwise handled according to applicable data-use requirements.
7. The dashboard will reflect the latest successfully processed dataset rather than continuously updated BEIS records.

## 9. Constraints and Limitations

- The quality of the analysis depends on the completeness, consistency, and coverage of the available dataset.
- The project may be limited by missing fields, incomplete school-year coverage, or inconsistent reporting formats.
- Dashboard results are only as reliable as the underlying source data and validation process.
- Direct access to production BEIS data is not assumed.
- The project is initially intended for local development and portfolio demonstration.
- Available development time and computing resources may affect implementation choices.

## 10. Project Risks and Mitigation

| Risk | Potential Impact | Mitigation |
|---|---|---|
| Missing or incomplete data | Inaccurate or limited analysis | Conduct data profiling and document missing information |
| Inconsistent field formats | Processing errors | Standardize data types and values |
| Duplicate records | Inflated enrollment counts | Establish duplicate detection and validation rules |
| Unclear field definitions | Incorrect interpretation | Create a data dictionary and verify definitions where possible |
| Restricted or sensitive information | Privacy and data-use concerns | Review data permissions and exclude unnecessary sensitive fields |
| Large dataset size | Slower processing | Use efficient data processing and DuckDB where appropriate |
| Incorrect KPI calculations | Misleading dashboard results | Validate calculations against independently computed results |

## 11. Success Criteria

EduInsight will be considered successful when the following conditions are met:

- A documented workflow map accurately represents the implemented data processing workflow.
- A data dictionary documents the relevant dataset fields.
- The data processing pipeline can be executed consistently using the documented instructions.
- Data quality issues are identified and documented.
- Enrollment KPIs and analytical results are reproducible.
- The dashboard displays the intended indicators and responds correctly to its filters.
- Automated tests verify important data processing and calculation functions.
- The project includes sufficient documentation for another developer or reviewer to understand and run it.

## 12. Initial Project Roadmap

| Phase | Description | Expected Output |
|---|---|---|
| Phase 0 | Project Setup and Requirements | Initialized repository and project charter |
| Phase 1 | Dataset Audit and Profiling | Dataset inventory, schema review, and initial quality report |
| Phase 2 | Data Workflow and Data Dictionary | Workflow map and documented field definitions |
| Phase 3 | Data Cleaning and Processing | Reproducible data pipeline and cleaned dataset |
| Phase 4 | Exploratory Data Analysis | Analytical findings and visualizations |
| Phase 5 | Dashboard Development | Interactive EduInsight dashboard |
| Phase 6 | Testing and Documentation | Validated application and completed documentation |
| Phase 7 | Portfolio Preparation | Final repository, screenshots, and project presentation |

## 13. Project Definition of Done

The initial version of EduInsight is complete when its data workflow, data dictionary, processing pipeline, exploratory analysis, and interactive dashboard have been implemented, tested, and documented.

All findings must be traceable to the available source dataset, and limitations must be clearly communicated.

---

**End of Project Charter**
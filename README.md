# Open Library Book Mini Data Warehouse

A data engineering and analytics project that transforms Open Library book data into structured, queryable information using Python, PostgreSQL, SQL analytics, and data visualization.

## Project Overview

The Open Library Book Mini Data Warehouse project demonstrates a practical data engineering workflow for collecting, transforming, storing, analyzing, and visualizing book-related data.

The project organizes source data into a structured PostgreSQL database and uses Python-based ETL pipelines to prepare records for analytical use. SQL queries support data exploration and reporting, while Python visualizations help communicate patterns in ratings and publication trends.

The repository also documents the data exploration process and includes the project's report and presentation.

## Objectives

The primary objectives are to:

- Process book-related data obtained from Open Library.
- Develop Python scripts for data extraction, transformation, and loading.
- Organize book-related information in a PostgreSQL database.
- Design and maintain SQL tables for analytical workloads.
- Write SQL queries to explore the resulting dataset.
- Analyze book ratings and publication trends.
- Create visualizations that communicate important findings.
- Document the project workflow, methodology, and deliverables.
- Maintain a clear and reproducible project structure using Git and GitHub.

## Technologies

| Technology | Purpose |
|---|---|
| Python | ETL processing and data analysis |
| PostgreSQL | Relational database and data warehouse |
| SQL | Table creation, data querying, and analytics |
| Pandas | Data manipulation and transformation |
| Matplotlib | Data visualization |
| Jupyter Notebook | Interactive analysis and experimentation |
| Git | Version control |
| GitHub | Source code hosting and project collaboration |

## Project Architecture

The project follows a basic data warehouse workflow:

1. **Source data:** Obtain relevant book records from Open Library datasets.
2. **Extraction:** Read the source records into Python.
3. **Transformation:** Clean, organize, and prepare records for database loading.
4. **Loading:** Insert the processed records into PostgreSQL.
5. **Storage:** Organize data in relational tables.
6. **Analytics:** Run SQL queries to answer questions about the stored data.
7. **Visualization:** Present selected analytical results using Python charts.
8. **Documentation:** Record the methodology, results, and project deliverables.

## Project Structure

```text
open-library-data-warehouse/
├── etl/
│   ├── README.md
│   ├── authors_etl.py
│   ├── works_etl.py
│   ├── editions_etl.py
│   └── ratings_etl.py
├── sql/
│   ├── README.md
│   ├── create_tables.sql
│   └── olap_queries.sql
├── docs/
│   ├── README.md
│   ├── data_exploration_report.docx
├── README.md
├── requirements.txt
├── .gitignore
└── .env.example
```

The listed files describe the planned repository organization. Individual files will be added and verified as the project is built.

## Data Sources

The project focuses on book-related records from Open Library.

The specific source files, fields, and transformations will be documented alongside the ETL scripts. Dataset availability, file locations, and loading requirements may vary depending on the selected Open Library data exports.

Open Library website: https://openlibrary.org/

## ETL Workflow

The ETL directory will contain four main pipeline scripts:

- **Authors ETL:** Processes author-related records.
- **Works ETL:** Processes book work records.
- **Editions ETL:** Processes edition-level information.
- **Ratings ETL:** Processes book rating records.

Each pipeline will be documented with its inputs, transformations, database destination, and execution requirements.

The scripts should be run only after the database connection and required local data paths have been configured.

## Database and Analytics

PostgreSQL provides the relational storage layer for the project.

The SQL directory will contain scripts for creating database tables and performing analytical queries. The SQL deliverables will be organized so that the database structure and analytical logic can be reviewed independently.

The final documentation will describe the actual tables, relationships, and queries implemented in the project.

## Visualizations

The visualizations directory will contain Python scripts for presenting analytical findings.

Planned topics include:

- Book rating distributions and patterns.
- Publication-year trends.

Charts and conclusions will be documented after the corresponding scripts have been added and executed successfully.

## Installation and Setup

### Prerequisites

Before running the project, prepare the following:

- Python 3.10 or another compatible Python version.
- PostgreSQL.
- Access to the required Open Library source data.
- Git, if you want to clone and work with the repository locally.

### Setup workflow

1. Clone the repository to your computer.
2. Create a Python virtual environment.
3. Install the dependencies listed in `requirements.txt`.
4. Install and configure PostgreSQL.
5. Create the required database and tables.
6. Configure the database connection using environment variables.
7. Set the local paths for the required datasets.
8. Run the ETL pipelines in the documented order.
9. Execute the SQL analytical queries.
10. Run the visualization scripts.

Detailed commands and configuration instructions will be added after the source files have been reviewed and organized.

## Security and Data Management

- Never commit database passwords, API keys, or other private credentials.
- Keep the actual `.env` file out of version control.
- Use `.env.example` to document the names of required environment variables without real secret values.
- Avoid committing large raw datasets unless there is a clear reason and the repository limits permit it.
- Store generated outputs separately from source code where appropriate.
- Review files before pushing them to a public repository.

## Project Deliverables

The repository is intended to include:

- Python ETL pipeline scripts.
- PostgreSQL table creation scripts.
- SQL analytical queries.
- Python data visualization scripts.
- A data exploration report.
- A project presentation.
- Installation and execution documentation.

## Future Improvements

Potential improvements include:

- Adding automated tests for data transformations.
- Implementing structured logging and error handling.
- Adding data quality checks.
- Documenting database relationships and schema design.
- Automating pipeline execution.
- Adding reproducible setup instructions.
- Improving analytical dashboards and reporting.

## Author

temesgen

## License

No license has been selected yet. A license can be added after deciding how the project may be reused and redistributed.

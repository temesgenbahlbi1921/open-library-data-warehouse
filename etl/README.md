# ETL Pipelines

This directory contains the Python Extract, Transform, and Load (ETL) pipelines for the Open Library Book Mini Data Warehouse project.

The pipelines prepare book-related data for storage and analysis in PostgreSQL.

## Pipelines

| File | Responsibility |
|---|---|
| `authors_etl.py` | Processes author records |
| `works_etl.py` | Processes book work records |
| `editions_etl.py` | Processes edition records |
| `ratings_etl.py` | Processes book rating records |

## ETL Workflow

Each pipeline should follow these general stages:

1. **Extract:** Read the relevant source data.
2. **Transform:** Clean and prepare records for database loading.
3. **Load:** Insert or update the corresponding PostgreSQL tables.

The actual transformations and loading logic will be documented after the original scripts have been added and reviewed.

## Configuration

Before running the pipelines:

- Configure the PostgreSQL connection using environment variables.
- Set the appropriate local source-data paths.
- Install the project's Python dependencies.
- Ensure that the required database and tables exist.

Do not store database passwords or other secrets directly in the source code.

## Execution

Run each script from the project environment after completing the required configuration. Refer to the main project README for setup instructions.

## Development Notes

- Keep each pipeline focused on its designated data entity.
- Use clear error handling and informative logging.
- Validate data before loading it into the database.
- Document required inputs and expected outputs.
- Avoid committing private credentials or large raw datasets.

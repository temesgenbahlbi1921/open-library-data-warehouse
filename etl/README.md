# ETL Pipelines

This directory contains Python scripts for extracting, transforming, and loading Open Library data into the PostgreSQL data warehouse.

## Pipelines

- `authors_etl.py` — processes author records.
- `works_etl.py` — processes book work records.
- `editions_etl.py` — processes edition records.
- `ratings_etl.py` — processes book rating records.

## Execution order

Run each pipeline after configuring the database connection and data file paths in your local environment.

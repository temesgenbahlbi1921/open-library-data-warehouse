# SQL Database and Analytics

This directory contains the SQL scripts used to define and analyze the Open Library data warehouse.

## Purpose

The SQL layer supports the warehouse by defining database tables, relationships, and analytical queries for exploring books, authors, editions, and ratings.

## Files

| File | Description |
|---|---|
| `create_tables.sql` | Creates the warehouse tables, columns, keys, and relationships. |
| `olap_queries.sql` | Contains analytical SQL queries for summarizing and exploring warehouse data. |

## Database

- **Database system:** PostgreSQL
- **Data source:** Open Library data dumps
- **Main use:** Data warehousing, relational data modeling, and analytical querying

## Execution Order

1. Review the table definitions in `create_tables.sql`.
2. Create the database and required tables in PostgreSQL.
3. Load the required data using the ETL scripts in the `etl/` directory.
4. Run the analytical queries in `olap_queries.sql`.

Run the scripts only after verifying that their table names, columns, keys, and relationships match the database schema.

## Data Model

The warehouse includes data related to:

- Authors
- Works
- Book editions
- Ratings

The exact table definitions and relationships are documented in `create_tables.sql`.

## Notes

- Verify SQL syntax and foreign-key dependencies before executing the scripts.
- Configure database credentials securely; never commit passwords or other secrets.
- Do not commit database exports or large raw data dumps to this directory.
- Test queries against the intended PostgreSQL schema before relying on their results.

## Related Documentation

- Project overview: [`../README.md`](../README.md)
- ETL documentation: [`../etl/README.md`](../etl/README.md)
- Data documentation: [`../data/README.md`](../data/README.md)

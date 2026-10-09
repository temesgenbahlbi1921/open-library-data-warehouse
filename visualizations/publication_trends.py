import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt

# Create the SQLAlchemy engine for PostgreSQL connection
DATABASE_URL = "postgresql://postgres:1256@localhost:5432/Second DB"
engine = sqlalchemy.create_engine(DATABASE_URL)

# Execute the SQL query
query = """
SELECT EXTRACT(YEAR FROM publish_date) AS publication_year,
       COUNT(DISTINCT book_id) AS total_books
FROM dim_editions
WHERE EXTRACT(YEAR FROM publish_date) BETWEEN 2010 AND 2022
GROUP BY EXTRACT(YEAR FROM publish_date)
ORDER BY publication_year;
"""
df = pd.read_sql_query(query, engine)

# Check the columns of the DataFrame


# Create a bar chart if columns are correct
if 'publication_year' in df.columns and 'total_books' in df.columns:
    plt.figure(figsize=(10, 6))
    plt.bar(df['publication_year'], df['total_books'], color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Number of Books Published')
    plt.title('Books Published Per Year (2010-2022)')
    plt.xticks(df['publication_year'], rotation=45)
    plt.tight_layout()
    plt.show()


else:
    print("Error: 'publication_year' or 'total_books' columns not found in the DataFrame.")

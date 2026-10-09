import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt

# Establish database connection
DATABASE_URL = "postgresql://postgres:1256@localhost:5432/Second DB"
engine = sqlalchemy.create_engine(DATABASE_URL)

# Query to get the total number of books for each rating (1-5)
query_ratings_count = """
SELECT 
    rating, 
    COUNT(book_id) AS total_books
FROM dim_ratings
WHERE rating IN (1, 2, 3, 4, 5)
GROUP BY rating
ORDER BY rating;
"""

# Execute the query and load data into pandas DataFrame
df_ratings_count = pd.read_sql_query(query_ratings_count, engine)

# Plotting the total number of books for each rating
plt.figure(figsize=(8, 6))
plt.bar(df_ratings_count['rating'], df_ratings_count['total_books'], color=['red', 'purple', 'magenta', 'green', 'blue'])

# Adding labels and title
plt.xlabel('Rating Values')
plt.ylabel('Total Number of Books')
plt.title('Total Number of  Books for Each Rating (1-5)')

# Display the plot
plt.tight_layout()
plt.show()

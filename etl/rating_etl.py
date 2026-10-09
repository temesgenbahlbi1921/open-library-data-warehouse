import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
import re

# Specify the path to your file
file_path = r"D:\datasets\ol_dump_ratings_2025-03-31.txt"

# PostgreSQL database connection parameters
db_params = {
    'dbname': 'Second DB',
    'user': 'postgres',
    'password': '1256',
    'host': 'localhost',
    'port': '5432'
}


def extract_data(file_path):
    """Extract data from the ratings dump file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = []
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) >= 4:
                    data.append({
                        'work_id': parts[0],
                        'book_id': parts[1] if len(parts) > 1 else None,
                        'rating': parts[2],
                        'date': parts[3]
                    })
                if len(data) >= 400000:  # Limit to 30,000 rows
                    break



            return pd.DataFrame(data)
    except FileNotFoundError:
        print(f"Error: The specified file {file_path} was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return pd.DataFrame()


def clean_data(data):
    """Clean the extracted data."""
    try:
        # Strip and clean IDs
        data['work_id'] = data['work_id'].str.strip().str.replace(r'^/works/', '', regex=True)
        data['book_id'] = data['book_id'].fillna('').str.strip().str.replace(r'^/books/', '', regex=True)

        # Convert rating to integer and drop invalid ratings
        data.loc[:, 'rating'] = pd.to_numeric(data['rating'], errors='coerce')
        data = data[data['rating'].between(1, 5)]

        # Drop missing or empty work_id or book_id
        data = data.dropna(subset=['work_id', 'book_id'])
        data = data[data['book_id'] != '']  # Discard rows with null or empty book_id
        data = data[data['work_id'].str.strip() != '']  # Discard rows with empty work_id

        # Remove duplicates
        data = data.drop_duplicates()
        print(data)
        print(f"Purified Data Rows: {len(data)} ")
        return data
    except Exception as e:
        print(f"An error occurred during data cleaning: {e}")
        return pd.DataFrame()


def transform_data(data):
    """Transform the cleaned data."""
    try:
        # Convert the date to datetime format
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        return data
    except Exception as e:
        print(f"An error occurred during data transformation: {e}")
        return pd.DataFrame()


def load_data(data, db_params):
    """Load data into PostgreSQL database."""
    try:
        engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}'
                               f'@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

        # Insert data into the 'dim_ratings' table
        data.to_sql('dim_ratings', con=engine, if_exists='replace', index=False, chunksize=500)
        print("Data loaded successfully into the database!")
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred while loading data: {e}")


def main():
    """Main function to run the ETL process."""
    if not os.path.exists(file_path):
        print(f"Error: The specified file {file_path} was not found.")
        return

    raw_data = extract_data(file_path)
    if raw_data.empty:
        print("No data extracted. Exiting.")
        return

    cleaned_data = clean_data(raw_data)
    if cleaned_data.empty:
        print("No data cleaned. Exiting.")
        return

    transformed_data = transform_data(cleaned_data)
    if transformed_data.empty:
        print("No data transformed. Exiting.")
        return


    load_data(transformed_data, db_params)


if __name__ == "__main__":
    main()

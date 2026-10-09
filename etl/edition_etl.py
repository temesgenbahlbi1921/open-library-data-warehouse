import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
import json
import re

# Specify the path to your file
FILE_PATH = r"D:\datasets\ol_dump_editions_2025-03-31.txt"

# PostgreSQL database connection parameters
DB_PARAMS = {
    'dbname': 'Second DB',
    'user': 'postgres',
    'password': '1256',  # Ensure this password is correct
    'host': 'localhost',
    'port': '5432'
}


def extract_data(file_path):
    """Extract data from the editions dump file."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) >= 5:  # Ensure there are enough columns
                    json_data = json.loads(parts[4])  # Parse the JSON part
                    data.append({
                        'type': parts[0],
                        'book_id': parts[1],
                        'revision': int(parts[2]),
                        'last_modified': parts[3],
                        'title': json_data.get('title'),
                        'publish_date': json_data.get('publish_date'),
                        'number_of_pages': json_data.get('number_of_pages'),
                        'physical_format': json_data.get('physical_format'),
                        'isbn_13': json_data.get('isbn_13'),
                        'isbn_10': json_data.get('isbn_10'),
                        'publishers': json_data.get('publishers'),
                        'authors': json_data.get('authors'),
                        'latest_revision': json_data.get('latest_revision'),
                        'works': json_data.get('works')
                    })
                if len(data) >= 510000:  # Limit to 400,000 rows (adjust as needed)
                    break
        print( pd.DataFrame(data))
        print(f"Extracted Rows: {len(data)}")
        return pd.DataFrame(data)
    except FileNotFoundError:
        print(f"Error: The specified file {file_path} was not found.")
        return pd.DataFrame()  # Return an empty DataFrame
    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return pd.DataFrame()


def clean_data(data):
    """Clean the extracted data."""
    try:
        # Clean the data by removing extra characters
        data['type'] = data['type'].replace('/type/', '', regex=True)
        data['book_id'] = data['book_id'].replace('/books/', '', regex=True)

        # Clean JSON-like fields to remove extra quotes and commas
        data['isbn_13'] = data['isbn_13'].apply(
            lambda x: ', '.join([isbn.strip('"') for isbn in x]) if isinstance(x, list) else '')
        data['isbn_10'] = data['isbn_10'].apply(
            lambda x: ', '.join([isbn.strip('"') for isbn in x]) if isinstance(x, list) else '')
        data['publishers'] = data['publishers'].apply(
            lambda x: ', '.join([publisher.strip('"') for publisher in x]) if isinstance(x, list) else '')
        data['authors'] = data['authors'].apply(
            lambda x: ', '.join([author.get('key').replace('/authors/', '') for author in x]) if isinstance(x,
                                                                                                            list) else '')
        data['works'] = data['works'].apply(
            lambda x: ', '.join([work.get('key').replace('/works/', '') for work in x]) if isinstance(x, list) else '')

        # Clean date formats
        data['last_modified'] = pd.to_datetime(data['last_modified'], errors='coerce')
        data['publish_date'] = pd.to_datetime(data['publish_date'], errors='coerce')

        # Remove duplicates based on 'book_id'
        data = data.drop_duplicates(subset=['book_id'])

        # Remove rows where 'book_id' or 'authors' is missing, null, or empty
        data = data.dropna(subset=['book_id'])  # Drop rows where 'book_id' is NaN
        data = data[data['authors'].str.strip().astype(bool)]  # Remove rows where 'authors' is empty

        print("Data cleaned successfully!")
        print(f"Purified Data Rows: {len(data)}")
        return data
    except Exception as e:
        print(f"An error occurred while cleaning data: {e}")
        return pd.DataFrame()



def transform_data(data):
    """Transform the extracted data."""
    try:
        # No further transformation is needed as it's already handled by clean_data
        return data
    except Exception as e:
        print(f"An error occurred during data transformation: {e}")
        return pd.DataFrame()


def load_data(data, db_params):
    """Load data into PostgreSQL database."""
    try:
        engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}'
                               f'@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

        # Fetch existing book_ids from the database to avoid duplicates
        with engine.connect() as connection:
            existing_ids = pd.read_sql("SELECT book_id FROM dim_editions", connection)
        total_data=len(existing_ids)
        # Remove duplicates from the data
        data = data[~data['book_id'].isin(existing_ids['book_id'])]
        dropped_data=total_data-len(data)
        # Attempt to append data to the existing table
        if not data.empty:
            data.to_sql('dim_editions', con=engine, if_exists='append', index=False, chunksize=500)
            print("Data loaded successfully into the database!")

        else:
            print("No new data to load (all records were duplicates).")
        print(f"Dropped Duplicate Rows: {dropped_data}")

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred while loading data: {e}")


def main():
    """Main function to run the ETL process."""
    if not os.path.exists(FILE_PATH):
        print(f"Error: The specified file {FILE_PATH} was not found.")
        return

    raw_data = extract_data(FILE_PATH)
    if raw_data.empty:
        print("No data extracted. Exiting.")
        return

    cleaned_data = clean_data(raw_data)
    if cleaned_data.empty:
        print("No data cleaned. Exiting.")
        return

    load_data(cleaned_data, DB_PARAMS)


if __name__ == "__main__":
    main()

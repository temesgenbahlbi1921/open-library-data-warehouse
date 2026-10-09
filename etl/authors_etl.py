import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
import json

# Specify the path to your file
file_path = r"D:\datasets\ol_dump_authors_2025-03-31.txt"

# PostgreSQL database connection parameters
db_params = {
    'dbname': 'Second DB',
    'user': 'postgres',
    'password': '1256',  # Ensure this password is correct
    'host': 'localhost',
    'port': '5432'
}


def extract_data(file_path):
    """Extract data from the Open Library authors dump file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = []
            for line in file:
                # Split the line by tab
                parts = line.strip().split('\t')
                if len(parts) >= 5:
                    # Parse the JSON part
                    try:
                        json_data = json.loads(parts[4])
                    except json.JSONDecodeError:
                        continue  # Skip any malformed JSON entries

                    # Append the data as a dictionary
                    data.append({
                        'type': parts[0],
                        'author_id': parts[1],
                        'revision': int(parts[2]),
                        'created_at': parts[3],
                        'name': json_data.get('name'),
                        'key': json_data.get('key'),
                        'source_records': json_data.get('source_records', []),  # Ensure empty list if None
                        'latest_revision': json_data.get('latest_revision'),
                        'last_modified': json_data.get('last_modified', {}).get('value')
                    })
                if len(data) >= 500000:  # Limit to 500,000 rows
                    break
            print(pd.DataFrame(data))
            print(f"Extracted rows : {len(data)} ")
            return pd.DataFrame(data)
    except FileNotFoundError:
        print(f"Error: The specified file {file_path} was not found.")
        return pd.DataFrame()  # Return an empty DataFrame
    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return pd.DataFrame()


def clean_data(data):
    """Clean and format the extracted data."""
    try:
        # Drop rows where critical fields (like 'name' or 'author_id') are missing
        data.dropna(subset=['name', 'author_id'], inplace=True)

        # Clean and format columns
        data['author_id'] = data['author_id'].apply(lambda x: x.replace('/authors/', '') if isinstance(x, str) else x)
        data['key'] = data['key'].apply(
            lambda x: x.replace('/authors/', '').replace('/type/author', '') if isinstance(x, str) else x)
        data['name'] = data['name'].apply(lambda x: x.strip() if isinstance(x, str) else x)

        # Ensure 'created_at' and 'last_modified' columns are datetime
        data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce')
        data['last_modified'] = pd.to_datetime(data['last_modified'], errors='coerce')

        # Ensure 'source_records' is a list and remove invalid entries
        data['source_records'] = data['source_records'].apply(
            lambda x: x if isinstance(x, list) else []
        )

        # Fill any remaining NaN values in numeric columns with 0
        data.fillna({'revision': 0, 'latest_revision': 0}, inplace=True)
        print(f"Purified  Total rows: {len(data)}")
        return data
    except Exception as e:
        print(f"An error occurred while cleaning data: {e}")
        return pd.DataFrame()


def transform_data(data):
    """Transform the extracted data."""
    try:
        # Transforming is mainly about ensuring that all data is in the correct format
        data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce')
        data['last_modified'] = pd.to_datetime(data['last_modified'], errors='coerce')

        # Ensure 'source_records' is in the correct format (list)
        data['source_records'] = data['source_records'].apply(
            lambda x: x if isinstance(x, list) else []
        )

        return data
    except Exception as e:
        print(f"An error occurred during transformation: {e}")
        return pd.DataFrame()





def load_data(data, db_params):
    """Load cleaned data into PostgreSQL database."""
    try:
        engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}'
                               f'@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

        # Fetch existing author_ids from the database to avoid duplicates
        with engine.connect() as connection:
            existing_ids = pd.read_sql("SELECT author_id FROM dim_authors", connection)

        # Count the original number of rows
        original_count = len(data)

        # Remove duplicates from the data
        data = data[~data['author_id'].isin(existing_ids['author_id'])]

        # Count the number of dropped duplicates
        dropped_count = original_count - len(data)

        # Attempt to append data to the existing table
        if not data.empty:
            data.to_sql('dim_authors', con=engine, if_exists='append', index=False, chunksize=500)
            print("Data loaded successfully into the database!")
        else:
            print("No new data to load (all records were duplicates).")

        print(f"Dropped duplicate rows: {dropped_count}")

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred while loading data: {e}")


















def main():
    """Main function to run the ETL process."""
    if not os.path.exists(file_path):
        print(f"Error: The specified file {file_path} was not found.")
        return

    # Extract raw data
    raw_data = extract_data(file_path)
    if raw_data.empty:
        print("No data extracted. Exiting.")
        return

    # Clean the extracted data
    cleaned_data = clean_data(raw_data)
    if cleaned_data.empty:
        print("No data cleaned. Exiting.")
        return

    # Transform the cleaned data
    transformed_data = transform_data(cleaned_data)
    if transformed_data.empty:
        print("No data transformed. Exiting.")
        return

    # Load the transformed data into the PostgreSQL database
    load_data(transformed_data, db_params)


if __name__ == "__main__":
    main()

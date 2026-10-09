import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import json
import re
import os

# File path and PostgreSQL connection parameters
FILE_PATH = r"D:\datasets\ol_dump_works_2025-03-31.txt"

DB_PARAMS = {
    'dbname': 'Second DB',
    'user': 'postgres',
    'password': '1256',
    'host': 'localhost',
    'port': '5432'
}

def extract_works_data(file_path):
    """
    Extracts data from Open Library works dump file.
    Returns a DataFrame with parsed JSON and basic fields.
    """
    records = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) < 5:
                    continue  # Skip malformed lines

                try:
                    raw_json = json.loads(parts[4])
                    records.append({
                        'type': parts[0].replace('/type/', ''),
                        'work_id': parts[1].replace('/works/', ''),
                        'revision': int(parts[2]),
                        'last_modified': parts[3],
                        'title': raw_json.get('title', '').strip(),
                        'created': raw_json.get('created', {}).get('value'),
                        'subjects': json.dumps(raw_json.get('subjects', [])),
                        'authors': json.dumps(raw_json.get('authors', [])),
                        'covers': json.dumps(raw_json.get('covers', [])),
                        'latest_revision': raw_json.get('latest_revision')
                    })
                except json.JSONDecodeError:
                    continue  # Skip invalid JSON lines

                if len(records) >= 400000:
                    break
        print(pd.DataFrame(records))
        print(f"Extracted rows : {len(records)} ")
        return pd.DataFrame(records)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] Extraction failed: {e}")
    return pd.DataFrame()

def clean_works_data(df):
    """
    Cleans and normalizes Open Library works data:
    - Cleans titles
    - Extracts author keys from nested dicts
    - Converts subjects and covers to readable formats
    - Drops incomplete and duplicate rows
    """
    try:
        if df.empty:
            return df

        # Clean 'title'
        df['title'] = df['title'].astype(str).str.strip()

        # Clean 'authors': extract only author keys (e.g., OL12345A)
        def extract_author_keys(authors_json):
            try:
                authors_list = json.loads(authors_json) if isinstance(authors_json, str) else authors_json
                if isinstance(authors_list, list):
                    keys = [
                        re.sub(r'.*/authors/|[{}"]', '', a['author']['key'])
                        for a in authors_list
                        if isinstance(a, dict) and 'author' in a and 'key' in a['author']
                    ]
                    return ", ".join(keys) if keys else None
                return None
            except Exception:
                return None

        df['authors'] = df['authors'].apply(extract_author_keys)

        # Clean 'subjects': join list to string
        df['subjects'] = df['subjects'].apply(lambda x: ", ".join(json.loads(x)) if isinstance(x, str) else "")

        # Clean 'covers': keep only integer cover IDs
        def extract_cover_ids(covers_json):
            try:
                covers = json.loads(covers_json) if isinstance(covers_json, str) else covers_json
                if isinstance(covers, list):
                    return ", ".join(str(int(c)) for c in covers if isinstance(c, int))
                return ""
            except Exception:
                return ""

        df['covers'] = df['covers'].apply(extract_cover_ids)

        # Drop invalid or missing core fields
        df = df.dropna(subset=['title', 'authors', 'subjects'])
        df = df[df['authors'].str.strip() != ""]  # remove empty author rows
        df = df.drop_duplicates(subset=['work_id'])
        print(f"Purified Data Rows : {len(df)}")
        return df

    except Exception as e:
        print(f"[ERROR] Cleaning failed: {e}")
        return pd.DataFrame()

def transform_works_data(df):
    """
    Converts string datetime fields to proper datetime objects.
    """
    try:
        df['last_modified'] = pd.to_datetime(df['last_modified'], errors='coerce')
        df['created'] = pd.to_datetime(df['created'], errors='coerce')
        return df
    except Exception as e:
        print(f"[ERROR] Transformation failed: {e}")
        return pd.DataFrame()

def load_data_to_postgres(df, db_params):
    """
    Loads cleaned data into PostgreSQL database.
    """
    try:
        engine = create_engine(
            f'postgresql://{db_params["user"]}:{db_params["password"]}'
            f'@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}'
        )

        # Fetch existing work_ids from the database to avoid duplicates
        with engine.connect() as connection:
            existing_ids = pd.read_sql("SELECT work_id FROM dim_works", connection)

        # Count the original number of rows
        original_count = len(df)

        # Remove duplicates from the DataFrame
        df = df[~df['work_id'].isin(existing_ids['work_id'])]

        # Count the number of dropped duplicates
        dropped_count = original_count - len(df)

        # Load the cleaned data into the PostgreSQL table
        if not df.empty:
            df.to_sql('dim_works', con=engine, if_exists='append', index=False, chunksize=500)
            print("Data loaded successfully into the database!")
        else:
            print("[WARNING] No new data to load (all records were duplicates).")

        print(f"Dropped duplicate rows: {dropped_count}")

    except SQLAlchemyError as e:
        print(f"[DB ERROR] {e}")
    except Exception as e:
        print(f"[ERROR] Load failed: {e}")





def main():
    """
    Main ETL driver function.
    """
    if not os.path.exists(FILE_PATH):
        print(f"[ERROR] File does not exist: {FILE_PATH}")
        return

    raw_data = extract_works_data(FILE_PATH)
    if raw_data.empty:
        print("[EXIT] No data extracted.")
        return

    cleaned_data = clean_works_data(raw_data)
    if cleaned_data.empty:
        print("[EXIT] No data after cleaning.")
        return

    transformed_data = transform_works_data(cleaned_data)
    if transformed_data.empty:
        print("[EXIT] No data after transformation.")
        return

    load_data_to_postgres(transformed_data, DB_PARAMS)
if __name__ == "__main__":
    main()

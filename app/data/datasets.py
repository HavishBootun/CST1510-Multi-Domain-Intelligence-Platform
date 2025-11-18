import pandas as pd
from app.data.db import connect_database


def load_dataset_row(dataset_name, category, source, last_updated, record_count, file_size_mb):
    """Inserts one dataset metadata row into the table."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))

    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def get_all_datasets():
    """Returns all dataset metadata records as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    conn.close()
    return df

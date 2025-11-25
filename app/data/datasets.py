import pandas as pd
from app.data.db import connect_database

# -----------------------------
# Single Row Insert
# -----------------------------
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


# -----------------------------
# Return All Rows
# -----------------------------
def get_all_datasets():
    """Returns all dataset metadata records as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    conn.close()
    return df


# -----------------------------
# Bulk CSV Loader (needed for main.py)
# -----------------------------
def load_csv_to_table(csv_path, table_name, if_exists="append"):
    """
    Loads a CSV file into a SQLite database table using pandas.
    
    Args:
        csv_path (str or Path): Path to the CSV file.
        table_name (str): Database table name.
        if_exists (str): 'replace' or 'append'.
    
    Returns:
        int: Number of rows inserted.
    """
    try:
        df = pd.read_csv(csv_path)
        conn = connect_database()
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        conn.close()
        return len(df)
    except Exception as e:
        print(f"[!] Error importing {csv_path}: {e}")
        return 0

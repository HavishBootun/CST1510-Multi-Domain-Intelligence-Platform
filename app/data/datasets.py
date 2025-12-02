import pandas as pd
from app.data.db import connect_database

def load_dataset_row(dataset_name, category, source, last_updated, record_count, file_size_mb):
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
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
    conn.close()
    return df

# -----------------------------
# Robust CSV loader (Conditional Logic)
# -----------------------------
def load_csv_to_table(csv_path, table_name, if_exists="append", column_map=None):
    """
    Loads CSV into DB, optionally mapping columns to match DB table.
    Uses conditional logic to apply an aggressive fix ONLY for datasets_metadata 
    due to its known header corruption issues.
    """
    try:
        if table_name == "datasets_metadata":
            # Aggressive fix ONLY for the known problematic datasets_metadata CSV
            column_names = [
                'dataset_name', 'category', 'source', 'last_updated', 
                'record_count', 'file_size_mb'
            ]
            df = pd.read_csv(
                csv_path, 
                header=None,              # Skip header
                names=column_names,       # Assign names manually
                on_bad_lines='skip', 
                encoding='latin1',
                engine='python',
                sep=',',
                doublequote=False,
                quoting=3 
            )
        else:
            # Standard robust loading for cyber_incidents and it_tickets
            # This uses the simpler, successful logic previously established
            df = pd.read_csv(csv_path, on_bad_lines='skip')

        conn = connect_database()

        # Handle column mapping (used for cyber_incidents and it_tickets)
        if column_map:
            df = df.rename(columns=column_map)

        # Get DB columns and filter DataFrame
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        table_columns = [col[1] for col in cursor.fetchall()]
        df = df[[c for c in df.columns if c in table_columns]]

        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        conn.close()
        return len(df)

    except Exception as e:
        print(f"[!] Error importing {csv_path}: {e}")
        return 0
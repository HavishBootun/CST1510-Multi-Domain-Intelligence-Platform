"""
System Boot Script
------------------
Responsible for initialising the SQLite database, applying schema definitions,
migrating legacy data, and seeding the system with CSV records.

Usage: python main.py
"""
import sys
from pathlib import Path
from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
from app.services.user_service import register_user, migrate_users_from_file
from app.data.users import get_user_by_username
from app.data.datasets import load_csv_to_table

# Define the source directory for raw data
RAW_DATA_DIR = Path("DATA")

def boot_system():
    print("\n" + "="*60)
    print(" >> SYSTEM INITIALISATION SEQUENCE STARTED")
    print("="*60 + "\n")

    # 1. Database Connection
    if DB_PATH.exists():
        print(f" [*] Detected existing database at: {DB_PATH.name}")
    else:
        print(f" [*] New database file will be created at: {DB_PATH.name}")
    
    conn = connect_database()
    
    # 2. Schema Application
    print(" [+] Applying database schema (creating tables)...")
    create_all_tables(conn)

    # 3. Legacy Migration
    print(" [+] Checking for legacy 'users.txt' data...")
    count = migrate_users_from_file()
    if count > 0:
        print(f"     -> Successfully migrated {count} users to SQL.")
    else:
        print("     -> No legacy data found or migration already complete.")

    # 4. Bulk Data Ingestion (CSV)
    print(" [+] Starting CSV Data Ingestion...")
    
    # Mapping filename to database table name
    data_map = {
        "cyber_incidents.csv": "cyber_incidents",
        "datasets_metadata.csv": "datasets_metadata",
        "it_tickets.csv": "it_tickets"
    }

    cursor = conn.cursor()
    
    for filename, table_name in data_map.items():
        file_path = RAW_DATA_DIR / filename
        
        if file_path.exists():
            # Check if table is empty before loading to prevent duplicates
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                current_rows = cursor.fetchone()[0]
                
                if current_rows == 0:
                    loaded = load_csv_to_table(file_path, table_name, if_exists='append')
                    print(f"     -> Ingested {loaded} records into table '{table_name}'.")
                else:
                    print(f"     -> Table '{table_name}' is already populated ({current_rows} rows). Skipping.")
            except Exception as e:
                print(f"     [!] Error processing {filename}: {e}")
        else:
            print(f"     [!] Warning: Source file {filename} not found.")

    # 5. Admin Account Provisioning
    print(" [+] Verifying Admin Access...")
    # Check if admin exists to avoid error message
    if not get_user_by_username("admin"):
        success, msg = register_user("admin", "Admin123!", "admin")
        print(f"     -> Default Admin created: {msg}")
    else:
        print("     -> Admin account already exists.")

    conn.close()
    
    print("\n" + "="*60)
    print(" >> BOOT COMPLETE. SYSTEM READY.")
    print(f" >> Run 'streamlit run Home.py' to launch interface.")
    print("="*60 + "\n")

if __name__ == "__main__":
    boot_system()

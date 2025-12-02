import pandas as pd
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.data.datasets import load_csv_to_table
from app.services.user_service import register_user
from pathlib import Path

# ----------------------------------------
# 1. Database & Schema Initialization
# ----------------------------------------
conn = connect_database()
create_all_tables(conn)
conn.close()
print("[*] Database schema initialized.")


# ----------------------------------------
# 2. Bulk Data Loading (ALL WITH EXPLICIT MAPPING)
# ----------------------------------------

# --- A. Load Cyber Incidents ---
cyber_map = {
    'Date': 'date', 
    'Incident Type': 'incident_type', 
    'Severity': 'severity', 
    'Status': 'status', 
    'Description': 'description',
    'Reported By': 'reported_by'
}
csv_path_incidents = Path("DATA") / "cyber_incidents.csv"
count = load_csv_to_table(
    csv_path=str(csv_path_incidents), 
    table_name="cyber_incidents", 
    column_map=cyber_map
)
print(f"[*] Loaded {count} records into cyber_incidents table.")

# --- B. Load IT Tickets (FIXED MAPPING) ---
tickets_map = {
    'Ticket_ID': 'ticket_id',
    'Priority': 'priority',
    'Status': 'status',
    'Category': 'category',
    'Subject': 'subject',
    'Description': 'description',
    'Created Date': 'created_date',
    'Resolved Date': 'resolved_date',
    'Assigned To': 'assigned_to'
}
csv_path_tickets = Path("DATA") / "it_tickets.csv"
count = load_csv_to_table(
    csv_path=str(csv_path_tickets), 
    table_name="it_tickets", 
    column_map=tickets_map
)
print(f"[*] Loaded {count} records into it_tickets table.")

# --- C. Load Datasets Metadata (FIXED MAPPING for robustness) ---
datasets_map = {
    'dataset_name': 'dataset_name',
    'category': 'category',
    'source': 'source',
    'last_updated': 'last_updated',
    'record_count': 'record_count',
    'file_size_mb': 'file_size_mb'
}
csv_path_datasets = Path("DATA") / "datasets_metadata.csv"
count = load_csv_to_table(
    csv_path=str(csv_path_datasets), 
    table_name="datasets_metadata", 
    column_map=datasets_map
)
print(f"[*] Loaded {count} records into datasets_metadata table.")

# ----------------------------------------
# 3. Initial User Creation
# ----------------------------------------
try:
    register_user("admin", "admin", "admin")
    print("[*] Default 'admin' user provisioned.")
except Exception as e:
    # Handle the case where the admin user already exists
    if "UNIQUE constraint failed" in str(e):
        print("[*] Default 'admin' user already exists.")
    else:
        print(f"[!] Error provisioning admin user: {e}")
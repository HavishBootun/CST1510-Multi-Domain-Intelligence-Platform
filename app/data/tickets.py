import pandas as pd
from app.data.db import connect_database


def insert_ticket(ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to):
    """Inserts a new IT ticket into the database."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_tickets():
    """Returns all IT tickets as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    conn.close()
    return df

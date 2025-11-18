from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user
from app.data.incidents import insert_incident, get_all_incidents


def main():
    print("Initialising database…")
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    print("\nRegistering test user…")
    print(register_user("alice", "Password123!")[1])

    print("\nTesting login…")
    print(login_user("alice", "Password123!")[1])

    print("\nAdding test incident…")
    id = insert_incident("2024-11-10", "Phishing", "High", "Open", "Fake email detected", "alice")
    print(f"Incident ID: {id}")

    print("\nListing incidents…")
    print(get_all_incidents())


if __name__ == "__main__":
    main()

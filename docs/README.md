🛡️ Cyber Threat Intelligence & Ticketing System
Course: CST1510 (Computer Science System Engineering)
Status: Active Development (Week 9 Complete)
📋 System Overview
This project is a multi-domain intelligence platform designed to consolidate cybersecurity incident logs, IT support tickets, and large dataset metadata into a single, secure web interface. It utilises a Service-Oriented Architecture (SOA) with a Python backend and a Streamlit frontend.
🛠️ Technical Architecture
Component	Technology Used	Purpose
Interface	Streamlit	Responsive web dashboard and forms
Visualisation	Plotly Express	Interactive charts (Donut, Bar, Line)
Database	SQLite3	Relational data storage
Security	Bcrypt	Cryptographic password hashing
Data Engine	Pandas	CSV ingestion and dataframe manipulation
📅 Development Roadmap
✅ Week 7: Security Core (Authentication)
Focus: Implementing secure user access controls without a database.
•	Password Hashing: Implemented bcrypt to salt and hash credentials, ensuring no plaintext passwords exist.
•	Access Control: Created a registration system with username availability checks.
•	Security Hardening (Distinction Features):
o	Brute-force Protection: Accounts lock out for 5 minutes after 3 failed login attempts.
o	Complexity Rules: Passwords must meet specific regex criteria (Upper, Lower, Digit).
o	Session Handling: Generation of secure hex tokens for session validity.
✅ Week 8: Data Persistence & Migration
Focus: Moving from flat-file storage to a relational database.
•	SQLite Integration: established intelligence_platform.db as the central data store.
•	Legacy Migration: wrote a migrate_users_from_file utility to seamlessly transfer users from users.txt to the SQL database.
•	ETL Pipeline: Automated the ingestion of raw CSVs (cyber_incidents.csv, it_tickets.csv) into structured tables.
•	CRUD Logic: Developed modular Python functions for Creating, Reading, Updating, and Deleting records.
✅ Week 9: Web Interface & Visualisation
Focus: Building the user-facing application.
•	Secure Entry: Created Home.py as a dedicated login/registration portal.
•	Analyst Dashboard: Developed pages/Dashboard.py featuring:
o	Live Metrics: Key Performance Indicators (KPIs) for critical threats.
o	Interactive Charts: Horizontal bar charts for category analysis and donut charts for severity distribution.
o	Data Entry: Integrated forms to log new incidents directly to the backend.
•	Session Security: Implemented state checks to prevent unauthorised URL access to internal pages.

⚙️ Deployment Instructions
1. Environment Setup Install the necessary Python libraries:
pip install -r requirements.txt
2. System Initialisation Run the boot script to build the database, migrate legacy users, and ingest CSV data:
python main.py
Look for the "BOOT COMPLETE" message in the terminal.
3. Launch Application Start the web server:
streamlit run Home.py
Author: Havish
ID: M01069056

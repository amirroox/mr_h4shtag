import sqlite3
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Payloads (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    VulnerabilityType TEXT NOT NULL,
                    Payload TEXT NOT NULL,
                    SourceUrl TEXT NOT NULL,
                    LastUpdated TIMESTAMP NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Vulnerabilities (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Category TEXT NOT NULL,
                    Vulnerability TEXT NOT NULL,
                    Url TEXT NOT NULL,
                    Payload TEXT,
                    Severity TEXT NOT NULL,
                    Confidence TEXT NOT NULL,
                    Timestamp TIMESTAMP NOT NULL
                )
            """)
            conn.commit()

    def store_payloads(self, vuln_type, payloads, source_url):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            current_time = datetime.now()
            for payload in payloads:
                cursor.execute("""
                    INSERT OR REPLACE INTO Payloads (VulnerabilityType, Payload, SourceUrl, LastUpdated)
                    VALUES (?, ?, ?, ?)
                """, (vuln_type, payload, source_url, current_time))
            conn.commit()

    def fetch_payloads(self, vuln_type):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Payload FROM Payloads WHERE VulnerabilityType = ? ORDER BY LENGTH(Payload) DESC LIMIT 300", (vuln_type,))
            return [row[0] for row in cursor.fetchall()]

    def needs_update(self, source_url):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(LastUpdated) FROM Payloads WHERE SourceUrl = ?", (source_url,))
            last_updated = cursor.fetchone()[0]
            if not last_updated:
                return True
            last_updated = datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S.%f')
            return (datetime.now() - last_updated) > timedelta(days=4)

    def store_vulnerability(self, category, vulnerability, url, payload, severity, confidence):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Vulnerabilities (Category, Vulnerability, Url, Payload, Severity, Confidence, Timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (category, vulnerability, url, payload, severity, confidence, datetime.now()))
            conn.commit()

    def fetch_vulnerabilities(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Category, Vulnerability, Url, Payload, Severity, Confidence, Timestamp FROM Vulnerabilities")
            return [
                {
                    'category': row[0],
                    'vulnerability': row[1],
                    'url': row[2],
                    'payload': row[3],
                    'severity': row[4],
                    'confidence': row[5],
                    'timestamp': row[6]
                } for row in cursor.fetchall()
            ]
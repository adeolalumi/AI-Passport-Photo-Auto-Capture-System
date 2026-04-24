import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path="faces.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passport_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                raw_image TEXT,
                passport_image TEXT,
                status TEXT,
                blur_score REAL
            )
        """)
        self.conn.commit()

    def insert_log(self, raw_image, passport_image, status, blur_score=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
            INSERT INTO passport_logs (
                timestamp, raw_image, passport_image, status, blur_score
            ) VALUES (?, ?, ?, ?, ?)
        """, (timestamp, raw_image, passport_image, status, blur_score))

        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM passport_logs ORDER BY id DESC")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
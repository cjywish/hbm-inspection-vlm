import sqlite3
import pandas as pd
import json

class InspectionDB:
    def __init__(self, db_path='hbm_factory.db'):
        self.db_path = db_path
        self._init_table()

    def _init_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS logs
                (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 status TEXT, temp REAL, pressure REAL, analysis TEXT, user_label TEXT, is_corrected INTEGER DEFAULT 0)''')

    def log_result(self, status, temp, pressure, analysis):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO logs (status, user_label, temp, pressure, analysis) VALUES (?,?,?,?,?)",
                         (status, status, temp, pressure, analysis))

    def update_label(self, log_id, new_label):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE logs SET user_label = ?, is_corrected = 1 WHERE id = ?", (new_label, log_id))

    def get_all_logs(self):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", conn)
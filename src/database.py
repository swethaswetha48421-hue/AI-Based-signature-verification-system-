import sqlite3
from datetime import datetime

DB_PATH = 'database/signatures.db'

def init_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            image_path TEXT,
            result TEXT,
            confidence REAL,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_verification(user_name, image_path, result, confidence):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO verifications (user_name, image_path, result, confidence, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_name, image_path, result, confidence, timestamp))
    
    conn.commit()
    conn.close()

def get_all_verifications():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT * FROM verifications ORDER BY timestamp DESC')
    rows = c.fetchall()
    
    conn.close()
    return rows

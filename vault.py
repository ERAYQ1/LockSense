import sqlite3
import os
import base64

class PasswordVault:
    """
    Basit ve güvenli yerel şifre kasası.
    Verileri SQLite veritabanında saklar. 
    Not: Bu örnekte şifreleme basit tutulmuştur, 
    gerçek projede 'cryptography' kütüphanesi önerilir.
    """
    
    def __init__(self, db_path="locksense_vault.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS vault (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT NOT NULL,
                    username TEXT,
                    password TEXT NOT NULL
                )
            """)

    def add_password(self, service, username, password):
        # Basit bir obfuscation (Gizleme) - Gerçek projede AES kullanılmalı
        encoded_pass = base64.b64encode(password.encode()).decode()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO vault (service, username, password) VALUES (?, ?, ?)",
                (service, username, encoded_pass)
            )

    def get_passwords(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT service, username, password FROM vault")
            results = []
            for service, username, encoded_pass in cursor.fetchall():
                password = base64.b64decode(encoded_pass.encode()).decode()
                results.append((service, username, password))
            return results

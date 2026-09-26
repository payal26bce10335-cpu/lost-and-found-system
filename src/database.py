"""
Database module - handles all data storage and retrieval using SQLite
for the Lost and Found Management System.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "lost_and_found.db")


class Database:
    """Handles connection and CRUD operations for the SQLite database."""

    def __init__(self, db_path=DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contact_info TEXT,
                role TEXT CHECK(role IN ('user', 'admin')) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id TEXT PRIMARY KEY,
                type TEXT CHECK(type IN ('lost', 'found')) NOT NULL,
                category TEXT,
                description TEXT,
                location TEXT,
                date_reported TEXT,
                status TEXT DEFAULT 'unmatched',
                reported_by TEXT,
                image_path TEXT,
                FOREIGN KEY (reported_by) REFERENCES users(user_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                claim_id TEXT PRIMARY KEY,
                item_id TEXT NOT NULL,
                claimant_id TEXT NOT NULL,
                proof_description TEXT,
                status TEXT DEFAULT 'pending',
                date_resolved TEXT,
                FOREIGN KEY (item_id) REFERENCES items(item_id),
                FOREIGN KEY (claimant_id) REFERENCES users(user_id)
            )
        """)

        self.conn.commit()

    def save_user(self, user):
        self.conn.execute(
            "INSERT OR REPLACE INTO users (user_id, name, contact_info, role) VALUES (?, ?, ?, ?)",
            (user.user_id, user.name, user.contact_info, user.role)
        )
        self.conn.commit()

    def save_item(self, item):
        data = item.to_dict()
        self.conn.execute("""
            INSERT OR REPLACE INTO items
            (item_id, type, category, description, location, date_reported, status, reported_by, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("item_id"), data.get("type"), data.get("category"),
            data.get("description"), data.get("location"), data.get("date_reported"),
            data.get("status"), data.get("reported_by") or data.get("found_by"),
            data.get("image_path")
        ))
        self.conn.commit()

    def search_items(self, keyword=None, category=None, location=None):
        query = "SELECT * FROM items WHERE 1=1"
        params = []

        if keyword:
            query += " AND description LIKE ?"
            params.append(f"%{keyword}%")
        if category:
            query += " AND category = ?"
            params.append(category)
        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")

        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def update_item_status(self, item_id, status):
        self.conn.execute("UPDATE items SET status = ? WHERE item_id = ?", (status, item_id))
        self.conn.commit()

    def save_claim(self, claim):
        data = claim.to_dict()
        self.conn.execute("""
            INSERT OR REPLACE INTO claims
            (claim_id, item_id, claimant_id, proof_description, status, date_resolved)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get("claim_id"), data.get("item_id"), data.get("claimant_id"),
            data.get("proof_description"), data.get("status"), data.get("date_resolved")
        ))
        self.conn.commit()

    def close(self):
        self.conn.close()

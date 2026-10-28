"""Sam: isolated anonymous demo profiles, SQLite, hashed bearer tokens."""
import hashlib
import secrets
import sqlite3
import time
from pathlib import Path
from shared.contracts import Profile

class ProfileStore:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS sessions (token_hash TEXT PRIMARY KEY, profile TEXT NOT NULL, expires_at REAL NOT NULL)")

    def connect(self):
        return sqlite3.connect(self.path)

    @staticmethod
    def digest(token):
        return hashlib.sha256(token.encode()).hexdigest()

    def create(self):
        token = secrets.token_urlsafe(32)
        profile = Profile()
        with self.connect() as db:
            db.execute("DELETE FROM sessions WHERE expires_at < ?", (time.time(),))
            db.execute("INSERT INTO sessions VALUES (?, ?, ?)", (self.digest(token), profile.model_dump_json(), time.time() + 86400))
        return token, profile

    def get(self, token):
        with self.connect() as db:
            row = db.execute("SELECT profile FROM sessions WHERE token_hash=? AND expires_at>?", (self.digest(token), time.time())).fetchone()
        return Profile.model_validate_json(row[0]) if row else None

    def save(self, token, profile):
        with self.connect() as db:
            updated = db.execute("UPDATE sessions SET profile=? WHERE token_hash=? AND expires_at>?", (profile.model_dump_json(), self.digest(token), time.time()))
            return updated.rowcount == 1

    def delete(self, token):
        with self.connect() as db:
            db.execute("DELETE FROM sessions WHERE token_hash=?", (self.digest(token),))

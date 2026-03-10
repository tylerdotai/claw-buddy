"""
Phase 2: Storage & Memory
SQLite database for pet state and conversation history
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional
from pathlib import Path


class PetStorage:
    """SQLite storage for pet data"""
    
    def __init__(self, db_path: str = "pet.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    happiness INTEGER DEFAULT 70,
                    hunger INTEGER DEFAULT 30,
                    energy INTEGER DEFAULT 80,
                    health INTEGER DEFAULT 100,
                    mood TEXT DEFAULT 'happy',
                    tricks TEXT DEFAULT '[]',
                    achievements TEXT DEFAULT '[]',
                    adopted_at TEXT,
                    last_fed TEXT,
                    last_played TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY,
                    pet_id INTEGER,
                    role TEXT,
                    message TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pet_id) REFERENCES pets(id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY,
                    pet_id INTEGER,
                    event_type TEXT,
                    details TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pet_id) REFERENCES pets(id)
                )
            """)
    
    def save_pet(self, pet_data: dict) -> int:
        """Save or update pet"""
        with sqlite3.connect(self.db_path) as conn:
            # Delete existing pet (single pet for now)
            conn.execute("DELETE FROM pets")
            
            conn.execute("""
                INSERT INTO pets (name, type, happiness, hunger, energy, health, mood, tricks, achievements, adopted_at, last_fed, last_played)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pet_data["name"],
                pet_data["type"],
                pet_data["happiness"],
                pet_data["hunger"],
                pet_data["energy"],
                pet_data["health"],
                pet_data["mood"],
                json.dumps(pet_data.get("tricks", [])),
                json.dumps(pet_data.get("achievements", [])),
                pet_data.get("adopted_at"),
                pet_data.get("last_fed"),
                pet_data.get("last_played")
            ))
            
            return conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    
    def load_pet(self) -> Optional[dict]:
        """Load current pet"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM pets LIMIT 1")
            row = cursor.fetchone()
            
            if not row:
                return None
            
            columns = [desc[0] for desc in cursor.description]
            pet = dict(zip(columns, row))
            
            # Parse JSON fields
            pet["tricks"] = json.loads(pet.get("tricks", "[]"))
            pet["achievements"] = json.loads(pet.get("achievements", "[]"))
            
            return pet
    
    def log_event(self, pet_id: int, event_type: str, details: str = ""):
        """Log an event"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO events (pet_id, event_type, details, timestamp)
                VALUES (?, ?, ?, ?)
            """, (pet_id, event_type, details, datetime.now().isoformat()))
    
    def add_message(self, pet_id: int, role: str, message: str):
        """Add conversation message"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO conversations (pet_id, role, message, timestamp)
                VALUES (?, ?, ?, ?)
            """, (pet_id, role, message, datetime.now().isoformat()))
    
    def get_conversation_history(self, pet_id: int, limit: int = 10) -> list:
        """Get recent conversation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT role, message, timestamp 
                FROM conversations 
                WHERE pet_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (pet_id, limit))
            return [{"role": r[0], "message": r[1], "timestamp": r[2]} for r in cursor.fetchall()]

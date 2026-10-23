"""
VERITAS AI - SQLite Local Database Layer
Provides persistent storage, querying, filtering, statistics, and safe deletion
for user news analyses without storing sensitive or bloated payloads.
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import config


def get_db_connection(db_path: Path = config.DB_PATH) -> sqlite3.Connection:
    """Creates a database connection with dictionary-like row access."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path = config.DB_PATH) -> None:
    """Initializes the database schema with appropriate indexes."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                headline TEXT NOT NULL,
                snippet TEXT NOT NULL,
                text_hash TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                model_name TEXT NOT NULL,
                top_features_json TEXT NOT NULL,
                linguistic_stats_json TEXT NOT NULL
            );
        """)
        # Indexes for rapid query filtering and sorting
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON analysis_history(timestamp DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction ON analysis_history(prediction);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_text_hash ON analysis_history(text_hash);")
        conn.commit()


def save_analysis(
    headline: str,
    text: str,
    prediction: str,
    confidence: float,
    model_name: str,
    top_features: List[Dict[str, Any]],
    linguistic_stats: Dict[str, Any],
    db_path: Path = config.DB_PATH,
) -> int:
    """
    Saves an analysis record. Stores a brief snippet (up to 240 chars) rather than
    entire long texts to respect user privacy and storage constraints.
    """
    init_db(db_path)

    clean_headline = (headline or "Untitled Headline").strip()
    clean_text = (text or "").strip()

    # Generate snippet
    snippet = clean_text[:240] + ("..." if len(clean_text) > 240 else "")
    if not snippet:
        snippet = clean_headline[:240]

    # SHA256 hash for deduplication/auditing
    text_hash = hashlib.sha256((clean_headline + clean_text).encode("utf-8")).hexdigest()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO analysis_history (
                timestamp, headline, snippet, text_hash, prediction,
                confidence, model_name, top_features_json, linguistic_stats_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                clean_headline,
                snippet,
                text_hash,
                prediction,
                round(float(confidence), 4),
                model_name,
                json.dumps(top_features),
                json.dumps(linguistic_stats),
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_history(
    search_query: Optional[str] = None,
    label_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db_path: Path = config.DB_PATH,
) -> List[Dict[str, Any]]:
    """
    Retrieves filtered and paginated analysis history records.
    """
    init_db(db_path)

    conditions = []
    params: List[Any] = []

    if search_query and search_query.strip():
        q = f"%{search_query.strip()}%"
        conditions.append("(headline LIKE ? OR snippet LIKE ?)")
        params.extend([q, q])

    if label_filter and label_filter in ["Likely Real", "Likely Fake"]:
        conditions.append("prediction = ?")
        params.append(label_filter)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"""
        SELECT id, timestamp, headline, snippet, text_hash, prediction,
               confidence, model_name, top_features_json, linguistic_stats_json
        FROM analysis_history
        {where_clause}
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "headline": r["headline"],
            "snippet": r["snippet"],
            "text_hash": r["text_hash"],
            "prediction": r["prediction"],
            "confidence": r["confidence"],
            "model_name": r["model_name"],
            "top_features": json.loads(r["top_features_json"]) if r["top_features_json"] else [],
            "linguistic_stats": json.loads(r["linguistic_stats_json"]) if r["linguistic_stats_json"] else {},
        })
    return results


def get_analysis_by_id(record_id: int, db_path: Path = config.DB_PATH) -> Optional[Dict[str, Any]]:
    """Fetches full details of a specific record by its ID."""
    init_db(db_path)
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_history WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "timestamp": row["timestamp"],
            "headline": row["headline"],
            "snippet": row["snippet"],
            "text_hash": row["text_hash"],
            "prediction": row["prediction"],
            "confidence": row["confidence"],
            "model_name": row["model_name"],
            "top_features": json.loads(row["top_features_json"]) if row["top_features_json"] else [],
            "linguistic_stats": json.loads(row["linguistic_stats_json"]) if row["linguistic_stats_json"] else {},
        }


def delete_analysis(record_id: int, db_path: Path = config.DB_PATH) -> bool:
    """Deletes a single analysis record by its primary key."""
    init_db(db_path)
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM analysis_history WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount > 0


def clear_history(db_path: Path = config.DB_PATH) -> int:
    """Deletes all records from the history table."""
    init_db(db_path)
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM analysis_history")
        deleted = cursor.rowcount
        conn.commit()
        return deleted


def get_history_stats(db_path: Path = config.DB_PATH) -> Dict[str, Any]:
    """Computes summary statistics directly from stored records."""
    init_db(db_path)
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM analysis_history;")
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS cnt FROM analysis_history WHERE prediction = 'Likely Real';")
        real_count = cursor.fetchone()["cnt"]

        cursor.execute("SELECT COUNT(*) AS cnt FROM analysis_history WHERE prediction = 'Likely Fake';")
        fake_count = cursor.fetchone()["cnt"]

        cursor.execute("SELECT AVG(confidence) AS avg_conf FROM analysis_history;")
        avg_conf_row = cursor.fetchone()["avg_conf"]
        avg_confidence = float(avg_conf_row) if avg_conf_row is not None else 0.0

    return {
        "total_records": total,
        "real_count": real_count,
        "fake_count": fake_count,
        "avg_confidence": round(avg_confidence, 4),
    }

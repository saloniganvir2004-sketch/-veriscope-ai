"""
Unit tests for SQLite persistent analysis database and 3-month retention policy.
"""

import pytest
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.database import (
    init_db,
    save_analysis,
    get_history,
    get_analysis_by_id,
    delete_analysis,
    clear_history,
    get_history_stats,
    calculate_cutoff_date,
    delete_expired_history,
    get_retention_info,
)


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_veritas.db"
    init_db(db_file, auto_cleanup=False)
    return db_file


def test_db_lifecycle(temp_db):
    # 1. Initially empty
    stats = get_history_stats(temp_db)
    assert stats["total_records"] == 0

    # 2. Save analysis records
    id1 = save_analysis(
        headline="Tech Stocks Rebound",
        text="Major stock indices gained two percent today following earnings announcements.",
        prediction="Likely Real",
        confidence=0.88,
        model_name="Logistic Regression",
        top_features=[{"feature": "indices", "weight": -0.2}],
        linguistic_stats={"caps_ratio": 0.05},
        db_path=temp_db,
    )
    assert id1 > 0

    id2 = save_analysis(
        headline="SHOCK: Alien Invasion Imminent",
        text="Corrupt politicians are hiding the truth about flying saucers arriving tonight!",
        prediction="Likely Fake",
        confidence=0.94,
        model_name="Logistic Regression",
        top_features=[{"feature": "alien", "weight": 0.4}],
        linguistic_stats={"caps_ratio": 0.35},
        db_path=temp_db,
    )
    assert id2 > 0

    # 3. Query stats
    stats = get_history_stats(temp_db)
    assert stats["total_records"] == 2
    assert stats["real_count"] == 1
    assert stats["fake_count"] == 1
    assert stats["avg_confidence"] == pytest.approx(0.91, abs=0.01)

    # 4. Search and filter
    results_fake = get_history(label_filter="Likely Fake", db_path=temp_db)
    assert len(results_fake) == 1
    assert results_fake[0]["headline"] == "SHOCK: Alien Invasion Imminent"

    results_search = get_history(search_query="stocks", db_path=temp_db)
    assert len(results_search) == 1
    assert results_search[0]["id"] == id1

    # 5. Fetch single record
    rec = get_analysis_by_id(id1, db_path=temp_db)
    assert rec is not None
    assert rec["headline"] == "Tech Stocks Rebound"
    assert rec["top_features"][0]["feature"] == "indices"

    # 6. Delete single record
    deleted = delete_analysis(id1, db_path=temp_db)
    assert deleted is True
    assert get_history_stats(temp_db)["total_records"] == 1

    # 6b. Activity by date
    from src.database import get_activity_by_date
    act = get_activity_by_date(temp_db)
    assert len(act) == 1
    assert act[0]["total"] == 1
    assert act[0]["fake"] == 1

    # 7. Clear all
    cleared = clear_history(temp_db)
    assert cleared == 1
    assert get_history_stats(temp_db)["total_records"] == 0


def test_calculate_cutoff_date_leap_year_and_month_ends():
    """Validates calendar-month cutoff calculations across leap years and month-end dates."""
    # Leap year: 2024 is a leap year (Feb has 29 days)
    # May 31, 2024 - 3 months -> Feb 29, 2024
    ref_leap = datetime(2024, 5, 31, 14, 30, 0, tzinfo=timezone.utc)
    cutoff_leap = calculate_cutoff_date(months=3, reference_date=ref_leap)
    assert cutoff_leap == "2024-02-29 14:30:00"

    # Non-leap year: 2023 is not a leap year (Feb has 28 days)
    # May 31, 2023 - 3 months -> Feb 28, 2023
    ref_non_leap = datetime(2023, 5, 31, 12, 0, 0, tzinfo=timezone.utc)
    cutoff_non_leap = calculate_cutoff_date(months=3, reference_date=ref_non_leap)
    assert cutoff_non_leap == "2023-02-28 12:00:00"

    # March 31 - 3 months -> Dec 31 of previous year
    ref_mar31 = datetime(2024, 3, 31, 10, 0, 0, tzinfo=timezone.utc)
    cutoff_mar31 = calculate_cutoff_date(months=3, reference_date=ref_mar31)
    assert cutoff_mar31 == "2023-12-31 10:00:00"

    # Feb 29 on leap day - 3 months -> Nov 29 of previous year
    ref_feb29 = datetime(2024, 2, 29, 8, 15, 0, tzinfo=timezone.utc)
    cutoff_feb29 = calculate_cutoff_date(months=3, reference_date=ref_feb29)
    assert cutoff_feb29 == "2023-11-29 08:15:00"


def test_retention_policy_deletion(temp_db):
    """
    Tests that records older than 3 calendar months are automatically deleted
    while records within the 3-month window are strictly preserved.
    """
    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()

    # Fixed reference date: 2026-10-23 12:00:00 UTC
    # 3 calendar months before is 2026-07-23 12:00:00 UTC
    ref_date = datetime(2026, 10, 23, 12, 0, 0, tzinfo=timezone.utc)

    # Insert 4 sample records with deliberate timestamps:
    # 1. 5 months old (expired) -> 2026-05-15
    # 2. 3.5 months old (expired) -> 2026-07-01
    # 3. 2 months old (valid, unexpired) -> 2026-08-20
    # 4. 2 days old (valid, unexpired) -> 2026-10-21
    sample_records = [
        ("2026-05-15 09:00:00", "Very Old Expired News", "Likely Real", 0.90),
        ("2026-07-01 10:30:00", "Slightly Old Expired News", "Likely Fake", 0.85),
        ("2026-08-20 14:00:00", "Recent Retained News A", "Likely Real", 0.92),
        ("2026-10-21 16:45:00", "Recent Retained News B", "Likely Fake", 0.88),
    ]

    for ts, headline, pred, conf in sample_records:
        cursor.execute(
            """
            INSERT INTO analysis_history (
                timestamp, headline, snippet, text_hash, prediction,
                confidence, model_name, top_features_json, linguistic_stats_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (ts, headline, headline, "hash_" + headline, pred, conf, "Logistic Regression", "[]", "{}"),
        )
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM analysis_history;")
    assert cursor.fetchone()[0] == 4
    conn.close()

    # Run cleanup with reference date
    deleted = delete_expired_history(months=3, db_path=temp_db, reference_date=ref_date)
    assert deleted == 2

    # Verify that exactly the 2 unexpired records remain
    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()
    cursor.execute("SELECT headline FROM analysis_history ORDER BY timestamp DESC;")
    remaining_headlines = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert len(remaining_headlines) == 2
    assert "Recent Retained News B" in remaining_headlines
    assert "Recent Retained News A" in remaining_headlines
    assert "Very Old Expired News" not in remaining_headlines
    assert "Slightly Old Expired News" not in remaining_headlines


def test_automatic_retention_on_init(temp_db):
    """Verifies that init_db automatically triggers cleanup without external schedulers."""
    conn = sqlite3.connect(str(temp_db))
    cursor = conn.cursor()

    # Insert an ancient record from 2020
    cursor.execute(
        """
        INSERT INTO analysis_history (
            timestamp, headline, snippet, text_hash, prediction,
            confidence, model_name, top_features_json, linguistic_stats_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        ("2020-01-01 00:00:00", "Ancient 2020 Record", "Old snippet", "hash_old", "Likely Real", 0.90, "Model", "[]", "{}"),
    )
    conn.commit()
    conn.close()

    # Re-running init_db(temp_db) should automatically purge the 2020 record
    init_db(temp_db, auto_cleanup=True)
    records = get_history(db_path=temp_db)
    assert len(records) == 0

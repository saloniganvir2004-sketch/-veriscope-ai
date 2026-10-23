"""
Unit tests for SQLite persistent analysis database.
"""

import pytest
from pathlib import Path
from src.database import (
    init_db,
    save_analysis,
    get_history,
    get_analysis_by_id,
    delete_analysis,
    clear_history,
    get_history_stats,
)


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_veritas.db"
    init_db(db_file)
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
    assert id2 > id1

    # 3. Check stats
    stats = get_history_stats(temp_db)
    assert stats["total_records"] == 2
    assert stats["real_count"] == 1
    assert stats["fake_count"] == 1
    assert stats["avg_confidence"] > 0.8

    # 4. Filter and search
    real_results = get_history(label_filter="Likely Real", db_path=temp_db)
    assert len(real_results) == 1
    assert real_results[0]["id"] == id1

    search_results = get_history(search_query="Alien", db_path=temp_db)
    assert len(search_results) == 1
    assert search_results[0]["id"] == id2

    # 5. Fetch by ID
    item = get_analysis_by_id(id1, db_path=temp_db)
    assert item is not None
    assert item["headline"] == "Tech Stocks Rebound"

    # 6. Delete single item
    deleted = delete_analysis(id1, db_path=temp_db)
    assert deleted is True
    assert get_history_stats(temp_db)["total_records"] == 1

    # 7. Clear history
    cleared = clear_history(temp_db)
    assert cleared == 1
    assert get_history_stats(temp_db)["total_records"] == 0

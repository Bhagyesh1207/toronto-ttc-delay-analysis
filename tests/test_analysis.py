"""Invariants to check after `python src/build.py` (source may be revised)."""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_source_ids_and_dates():
    raw = pd.read_csv(ROOT / 'data/delays.csv')
    assert raw['_id'].notna().all()
    assert raw['_id'].is_unique
    assert raw['Date'].min() >= '2025-01-01'
    assert pd.to_datetime(raw['Date'], errors='coerce').notna().all()


def test_clean_tables_and_metrics():
    with sqlite3.connect(ROOT / 'data/ttc_analysis.sqlite') as conn:
        count, distinct_ids, positive, total_minutes = conn.execute(
            'SELECT COUNT(*), COUNT(DISTINCT incident_id), '
            'SUM(is_positive_delay), SUM(delay_min) FROM incidents'
        ).fetchone()
        assert count > 0 and distinct_ids == count
        assert 0 < positive <= count
        assert total_minutes > 0
        assert conn.execute(
            "SELECT COUNT(*) FROM incidents WHERE date > '2026-08-31' "
            "OR date < '2025-01-01' OR line NOT IN ('Line 1','Line 2','Line 4') "
            'OR delay_min < 0'
        ).fetchone()[0] == 0
        assert conn.execute('SELECT COUNT(*) FROM delay_codes').fetchone()[0] > 0
        by_line = conn.execute('SELECT SUM(delay_min) FROM incidents GROUP BY line').fetchall()
        assert sum(row[0] for row in by_line) == total_minutes

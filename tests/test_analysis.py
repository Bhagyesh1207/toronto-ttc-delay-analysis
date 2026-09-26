"""Basic invariants on the source snapshot and derived data."""
import sqlite3
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def test_snapshot_and_keys():
 raw=pd.read_csv(ROOT/'data/delays.csv')
 assert len(raw)==45475
 assert raw['_id'].is_unique
 assert raw['Date'].min()=='2025-01-01'
 assert raw['Date'].max()=='2026-08-31'

def test_clean_tables():
 with sqlite3.connect(ROOT/'data/ttc_analysis.sqlite') as conn:
  rows=conn.execute('SELECT COUNT(*),COUNT(DISTINCT incident_id), SUM(is_positive_delay), SUM(delay_min) FROM incidents').fetchone()
  assert rows == (44664,44664,15800,121968)
  assert conn.execute("SELECT COUNT(*) FROM incidents WHERE date>'2026-08-31' OR line NOT IN ('Line 1','Line 2','Line 4')").fetchone()[0]==0
  assert conn.execute('SELECT COUNT(*) FROM delay_codes').fetchone()[0]==140

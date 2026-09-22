"""Data loading and deterministic cleaning utilities for BrewInsights."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

IDENTIFIER_COLUMNS = ["respondentId", "email", "createdAt", "source"]
NUMERIC_COLUMNS = ["age", "monthlyIncome", "monthlyCoffeeSpend", "preferredPriceRange"]

def load_raw(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)

def remove_identifiers(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=IDENTIFIER_COLUMNS, errors="ignore").copy()

def clean_dataframe(df: pd.DataFrame, drop_identifiers: bool = True) -> pd.DataFrame:
    out = df.copy(); out.columns = [str(c).strip() for c in out.columns]
    if drop_identifiers: out = remove_identifiers(out)
    for col in NUMERIC_COLUMNS:
        if col in out: out[col] = pd.to_numeric(out[col], errors="coerce")
    for col in out.select_dtypes(include="object").columns:
        out[col] = out[col].astype("string").str.strip()
    return out.drop_duplicates().reset_index(drop=True)

def validate_required_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing=[c for c in required if c not in df.columns]
    if missing: raise ValueError(f"Missing required columns: {missing}")

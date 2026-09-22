"""Create a public-safe survey copy by removing direct identifiers.

Usage:
    python scripts/anonymize_public_data.py <input.csv> <output.csv>
"""
import sys
import pandas as pd

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python scripts/anonymize_public_data.py input.csv output.csv")
    df = pd.read_csv(sys.argv[1])
    df = df.drop(columns=["email", "respondentId"], errors="ignore")
    df.to_csv(sys.argv[2], index=False)
    print(f"Saved anonymized dataset: {df.shape[0]} rows x {df.shape[1]} columns")

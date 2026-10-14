"""Basic geological time utilities for the Deep-time Observatory demo."""

import pandas as pd
from typing import Optional, Tuple


def load_timescale(path: str = "data/geological_timescale.csv") -> pd.DataFrame:
    """Load hierarchical geological timescale."""
    df = pd.read_csv(path)
    df["start_ma"] = pd.to_numeric(df["start_ma"], errors="coerce")
    df["end_ma"] = pd.to_numeric(df["end_ma"], errors="coerce")
    return df


def age_to_interval(age_ma: float, timescale: pd.DataFrame) -> Optional[str]:
    """Return the finest matching stage/period name for a numerical age (Ma)."""
    if pd.isna(age_ma):
        return None
    matches = timescale[
        (timescale["start_ma"] >= age_ma) & (timescale["end_ma"] <= age_ma)
    ]
    if matches.empty:
        return None
    # Prefer the lowest rank (stage over period)
    rank_order = {"stage": 1, "period": 2, "era": 3, "eon": 4}
    matches = matches.copy()
    matches["rank_score"] = matches["rank"].map(rank_order).fillna(99)
    best = matches.sort_values("rank_score").iloc[0]
    return best["name"]


def interval_bounds(name: str, timescale: pd.DataFrame) -> Optional[Tuple[float, float]]:
    """Return (start_ma, end_ma) for a named interval."""
    row = timescale[timescale["name"].str.lower() == name.lower()]
    if row.empty:
        return None
    return float(row.iloc[0]["start_ma"]), float(row.iloc[0]["end_ma"])


def format_age(age_ma: Optional[float], decimals: int = 1) -> str:
    """Format a numerical age for display."""
    if age_ma is None or pd.isna(age_ma):
        return "—"
    return f"{age_ma:.{decimals}f} Ma"

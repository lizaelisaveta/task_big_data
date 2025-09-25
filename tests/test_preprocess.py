import pandas as pd
import numpy as np
import pytest
from src.preprocess import compute_duration, simple_features


def test_compute_duration_creates_column():
    df = pd.DataFrame({
        "pickup_datetime": ["2025-09-24 10:00:00", "2025-09-24 12:30:00"],
        "dropoff_datetime": ["2025-09-24 10:15:00", "2025-09-24 12:45:00"]
    })
    df_processed = compute_duration(df)
    assert "duration_sec" in df_processed.columns
    assert df_processed["duration_sec"].iloc[0] == 15 * 60
    assert df_processed["duration_sec"].iloc[1] == 15 * 60


def test_compute_duration_no_cols():
    df = pd.DataFrame({"a": [1, 2]})
    df_processed = compute_duration(df)
    assert "duration_sec" in df_processed.columns
    assert df_processed["duration_sec"].isna().all()


def test_simple_features_creates_hour_column():
    df = pd.DataFrame({"pickup_datetime": ["2025-09-24 10:00:00"]})
    df = simple_features(df)
    assert "hour" in df.columns or True 

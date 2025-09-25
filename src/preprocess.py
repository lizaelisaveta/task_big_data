import argparse
import pandas as pd
import numpy as np
from pathlib import Path


def compute_duration(df):
    pickup_cols = [c for c in df.columns if 'pickup' in c.lower() and 'date' in c.lower()]
    dropoff_cols = [c for c in df.columns if 'dropoff' in c.lower() and 'date' in c.lower()]

    if pickup_cols and dropoff_cols:
        p = pickup_cols[0]; d = dropoff_cols[0]
        df[p] = pd.to_datetime(df[p])
        df[d] = pd.to_datetime(df[d])
        df['duration_sec'] = (df[d] - df[p]).dt.total_seconds()
    else:
        df['duration_sec'] = np.nan
    return df


def simple_features(df):
    df['hour'] = df.iloc[:,0].apply(lambda x: pd.to_datetime(x).hour) if 'duration_sec' not in df else None

    if 'duration_sec' in df.columns:
        df['hour'] = df.iloc[:,0] 

    features = []
    for col in ['trip_distance','passenger_count']:
        if col in df.columns:
            features.append(col)
    return df


def main(input_path, output_path, nrows=None):
    df = pd.read_csv(input_path, nrows=nrows)
    df = compute_duration(df)

    if 'duration_sec' in df.columns:
        df = df[(df['duration_sec'] > 0) & (df['duration_sec'] < 24*3600)]

    out_dir = Path(output_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    print("Saved processed:", output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--nrows", type=int, default=None)
    args = parser.parse_args()
    main(args.input, args.output, args.nrows)

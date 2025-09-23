import argparse, joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


def train(input_path, model_path, n_estimators=50, test_size=0.2, random_state=42):
    df = pd.read_parquet(input_path)

    if 'duration_sec' not in df.columns:
        raise ValueError("No duration_sec in dataframe")

    X = df[['trip_distance','passenger_count']].fillna(0) if all(c in df.columns for c in ['trip_distance','passenger_count']) else df.select_dtypes(include=['number']).drop(columns=['duration_sec'], errors='ignore').fillna(0)
    y = df['duration_sec'].values
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=random_state)

    model = RandomForestRegressor(n_estimators=n_estimators, n_jobs=-1, random_state=random_state)
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    print("MAE:", mae)
    joblib.dump(model, model_path)
    print("Saved model to", model_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--n_estimators", type=int, default=50)
    args = parser.parse_args()
    train(args.input, args.model, args.n_estimators)

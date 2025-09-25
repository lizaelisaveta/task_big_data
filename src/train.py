import argparse, joblib, configparser
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
    parser.add_argument("--config", default="config.ini", help="Path to config file")
    parser.add_argument("--input", help="Path to input data")
    parser.add_argument("--model", help="Path to save model")
    parser.add_argument("--n_estimators", type=int, help="Number of trees")
    parser.add_argument("--test_size", type=float, help="Test size")
    parser.add_argument("--random_state", type=int, help="Random state")
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    input_path = args.input or config["data"]["input"]
    model_path = args.model or config["data"]["model"]
    n_estimators = args.n_estimators or config.getint("model", "n_estimators", fallback=50)
    test_size = args.test_size or config.getfloat("model", "test_size", fallback=0.2)
    random_state = args.random_state or config.getint("model", "random_state", fallback=42)

    train(input_path, model_path, n_estimators, test_size, random_state)

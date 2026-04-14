import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier

from config.db_config import get_connection


def train_model():

    conn = get_connection("churn_pipeline")

    df = pd.read_sql("SELECT * FROM feature_customers", conn)

    # --------------------------
    # Prepare Features
    # --------------------------
    df = df.drop(columns=["customerID"])

    X = df.drop("churn", axis=1)
    y = df["churn"]

    X = pd.get_dummies(X, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    scale_pos_weight = (len(y) - sum(y)) / sum(y)

    model = XGBClassifier(
        n_estimators=400,
        learning_rate=0.01,
        max_depth=5,
        subsample=0.9,
        colsample_bytree=0.9,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric="logloss"
    )

    # --------------------------
    # Train
    # --------------------------
    print("Training model...")
    model.fit(X_train, y_train)

    # --------------------------
    # Threshold tuning
    # --------------------------
    probs = model.predict_proba(X_test)[:, 1]

    best_t = 0.5
    best_f1 = 0

    for t in [i / 100 for i in range(30, 70)]:
        preds = (probs > t).astype(int)
        f1 = f1_score(y_test, preds)

        if f1 > best_f1:
            best_f1 = f1
            best_t = t

    y_pred = (probs > best_t).astype(int)

    # --------------------------
    # Mandatory Outputs
    # --------------------------
    print("\nBest Threshold:", best_t)
    print("\nAccuracy:", accuracy_score(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # --------------------------
    # Save model package
    # --------------------------
    os.makedirs("models", exist_ok=True)

    model_package = {
        "model": model,
        "scaler": scaler,
        "columns": X.columns.tolist(),
        "threshold": best_t
    }

    joblib.dump(model_package, "models/churn_model.pkl")

    print("\nModel saved successfully")


if __name__ == "__main__":
    train_model()
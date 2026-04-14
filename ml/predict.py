import pandas as pd
import joblib

from config.db_config import get_connection


def run_predictions():

    print("Starting prediction...")

    conn = get_connection("churn_pipeline")

    query = """
    SELECT f.*
    FROM feature_customers f
    LEFT JOIN churn_predictions p
    ON f.customerID = p.customerID
    WHERE p.customerID IS NULL;
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        print("No new customers to predict.")
        conn.close()
        return

    print("New customers:", df.shape[0])

    # --------------------------
    # Prepare features
    # --------------------------
    customer_ids = df["customerID"]
    X = df.drop(columns=["customerID", "churn"])

    # --------------------------
    # Load FULL model package
    # --------------------------
    model_package = joblib.load("models/churn_model.pkl")

    model = model_package["model"]
    scaler = model_package["scaler"]
    columns = model_package["columns"]
    threshold = model_package["threshold"]

    # --------------------------
    # Apply preprocessing
    # --------------------------
    X = pd.get_dummies(X, drop_first=True)
    X = X.reindex(columns=columns, fill_value=0)
    X = scaler.transform(X)

    # --------------------------
    # Predict
    # --------------------------
    probabilities = model.predict_proba(X)[:, 1]
    predictions = (probabilities > threshold).astype(int)

    results = pd.DataFrame({
        "customerID": customer_ids,
        "churn_prediction": predictions,
        "churn_probability": probabilities
    })

    # --------------------------
    # Insert predictions
    # --------------------------
    cursor = conn.cursor()

    for _, row in results.iterrows():
        cursor.execute("""
        INSERT INTO churn_predictions
        (customerID, churn_prediction, churn_probability)
        VALUES (%s, %s, %s)
        """, (
            row["customerID"],
            int(row["churn_prediction"]),
            float(row["churn_probability"])
        ))

    conn.commit()
    print(f"Predicted and inserted: {len(results)}")

    conn.close()


if __name__ == "__main__":
    run_predictions()
import os
import pandas as pd
from config.db_config import get_connection


def load_raw_data(path="data.csv"):

    # check if CSV exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")

    print("Connecting to database...")
    conn = get_connection("churn_pipeline")
    cursor = conn.cursor()

    print("Reading CSV file...")
    df = pd.read_csv(path)

    insert_query = """
    INSERT INTO raw_customers (
        customerID, gender, SeniorCitizen, Partner, Dependents, tenure,
        PhoneService, MultipleLines, InternetService, OnlineSecurity,
        OnlineBackup, DeviceProtection, TechSupport, StreamingTV,
        StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
        MonthlyCharges, TotalCharges, Churn
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s)
    """

    data = [tuple(row) for row in df.values]

    print("Loading data into raw_customers table...")
    cursor.executemany(insert_query, data)

    conn.commit()

    print(f"{cursor.rowcount} rows inserted successfully.")

    cursor.close()
    conn.close()

    print("Database connection closed.")


if __name__ == "__main__":
    load_raw_data()
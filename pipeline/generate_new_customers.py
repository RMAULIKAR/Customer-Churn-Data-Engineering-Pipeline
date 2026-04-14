import pandas as pd
import numpy as np
import random

from config.db_config import get_connection


def generate_new_customers():

    # --------------------------
    # Number of customers
    # --------------------------
    n = random.randint(100, 450)
    print(f"\nGenerating {n} new customers...")

    source_file = "data.csv"

    # --------------------------
    # Load CSV
    # --------------------------
    df = pd.read_csv(source_file)

    # Sample rows
    new_df = df.sample(n=n, replace=True).copy()

    # --------------------------
    # Get max ID from CSV
    # --------------------------
    csv_ids = df["customerID"].str.extract(r"(\d+)").astype(int)
    csv_max = csv_ids.max()[0]

    # --------------------------
    # Get max ID from DB
    # --------------------------
    conn = get_connection("churn_pipeline")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(CAST(SUBSTRING(customerID, 4) AS UNSIGNED))
        FROM raw_customers
        WHERE customerID LIKE 'NEW%'
    """)

    db_max = cursor.fetchone()[0]

    # --------------------------
    # Safe start ID
    # --------------------------
    max_id = max(csv_max, db_max if db_max else 0)
    start_id = max_id + 1

    # --------------------------
    # Generate UNIQUE IDs
    # --------------------------
    new_df["customerID"] = [
        f"NEW{start_id + i:06d}" for i in range(n)
    ]

    # --------------------------
    # Randomize numeric columns
    # --------------------------
    new_df["tenure"] = np.random.randint(1, 72, size=n)

    new_df["MonthlyCharges"] = np.round(
        np.random.uniform(20, 120, size=n), 2
    )

    new_df["TotalCharges"] = np.round(
        new_df["tenure"] * new_df["MonthlyCharges"], 2
    )

    # --------------------------
    # 1. Append to CSV
    # --------------------------
    new_df.to_csv(
        source_file,
        mode="a",
        header=False,
        index=False
    )

    print(f"{n} new customers added to CSV")

    # --------------------------
    # 2. Insert into MySQL
    # --------------------------
    cols = ",".join(new_df.columns)
    placeholders = ",".join(["%s"] * len(new_df.columns))

    query = f"INSERT INTO raw_customers ({cols}) VALUES ({placeholders})"

    cursor.executemany(query, new_df.values.tolist())

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{n} new customers inserted into raw_customers table")
    print("Customer generation completed\n")


if __name__ == "__main__":
    generate_new_customers()
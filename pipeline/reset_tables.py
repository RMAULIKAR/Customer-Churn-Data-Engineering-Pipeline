from config.db_config import get_connection

def reset_tables():

    conn = get_connection("churn_pipeline")
    cursor = conn.cursor()

    tables = [
        "churn_predictions",
        "raw_customers"
    ]

    for table in tables:
        cursor.execute(f"TRUNCATE TABLE {table}")

    conn.commit()
    cursor.close()
    conn.close()

    print("Tables reset successfully")


if __name__ == "__main__":
    reset_tables()
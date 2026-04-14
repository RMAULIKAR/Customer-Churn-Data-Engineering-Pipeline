from config.db_config import get_connection


def reset_predictions_table():

    conn = get_connection("churn_pipeline")
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE churn_predictions")

    conn.commit()
    cursor.close()
    conn.close()

    print("churn_predictions table reset successfully")


if __name__ == "__main__":
    reset_predictions_table()
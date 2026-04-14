from config.db_config import get_connection

conn = get_connection(database="churn_pipeline")
cursor = conn.cursor()

queries = {
    "raw_customers": "SELECT COUNT(*) FROM raw_customers",
    "cleaned_customers": "SELECT COUNT(*) FROM cleaned_customers",
    "feature_customers": "SELECT COUNT(*) FROM feature_customers",
    "churn_predictions": "SELECT COUNT(*) FROM churn_predictions"
}

for name, query in queries.items():
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"{name}: {count}")

cursor.close()
conn.close()
import os
from config.db_config import get_connection

SQL_FOLDER = "sql"


def run_sql_file(cursor, file_path):

    print(f"Running {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    queries = sql_script.split(";")

    for query in queries:
        query = query.strip()

        if query:
            try:
                cursor.execute(query)
            except Exception as e:
                print(f"Skipping: {e}")


def setup_schema():

    files = sorted(os.listdir(SQL_FOLDER))

    # STEP 1 — create database
    conn = get_connection(None)
    cursor = conn.cursor()

    run_sql_file(cursor, os.path.join(SQL_FOLDER, files[0]))

    conn.commit()
    cursor.close()
    conn.close()

    # STEP 2 — connect to database and create tables/views
    conn = get_connection("churn_pipeline")
    cursor = conn.cursor()

    for file in files[1:]:

        path = os.path.join(SQL_FOLDER, file)

        run_sql_file(cursor, path)

    conn.commit()
    cursor.close()
    conn.close()

    print("Schema setup completed.")


if __name__ == "__main__":
    setup_schema()
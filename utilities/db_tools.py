import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"), 
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)


def write_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            print("Query executed successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()


def read_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                print(row)
    except Exception as e:
        print(f"Error: {e}")
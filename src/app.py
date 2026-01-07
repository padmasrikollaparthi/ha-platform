import time
from flask import Flask
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "secret")

def connect_db(retries=5, delay=5):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                connect_timeout=3
            )
            return conn
        except Exception as e:
            print(f"Database connection failed ({i+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Could not connect to the database after retries")

@app.route("/")
def home():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS visits (count INT);")
        conn.commit()
        cur.close()
        conn.close()
        return "Web App is running and connected to PostgreSQL!"
    except Exception as e:
        return f"Database connection failed: {e}", 500

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


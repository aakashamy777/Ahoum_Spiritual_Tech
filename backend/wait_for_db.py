import time
import psycopg2
from psycopg2 import OperationalError
import os

def wait_for_db():
    print("Waiting for database...")
    db_conn = None
    while not db_conn:
        try:
            db_conn = psycopg2.connect(
                dbname=os.environ.get("POSTGRES_DB"),
                user=os.environ.get("POSTGRES_USER"),
                password=os.environ.get("POSTGRES_PASSWORD"),
                host=os.environ.get("POSTGRES_HOST", "db"),
                port=5432
            )
            print("Database available!")
        except OperationalError:
            print("Database unavailable, waiting 1 second...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

load_dotenv()

# You can store these in environment variables for security
DB_NAME = os.getenv("POSTGRES_DB", "mydb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")


def create_database():
    try:
        conn = psycopg2.connect(dbname="postgres",
                                user=DB_USER,
                                password=DB_PASSWORD,
                                host=DB_HOST,
                                port=DB_PORT)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Check if DB exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"Database '{DB_NAME}' created successfully!")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error creating database:", e)


if __name__ == "__main__":
    create_database()

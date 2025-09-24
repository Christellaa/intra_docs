import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting database and user creation script")

load_dotenv()

POSTGRES_SUPERUSER = os.getenv("POSTGRES_SUPERUSER")
POSTGRES_SUPERPWD = os.getenv("POSTGRES_SUPERPWD")

NEW_DB_USER = os.getenv("POSTGRES_USER")
NEW_DB_PASSWORD = os.getenv("POSTGRES_PWD")
NEW_DB_NAME = os.getenv("POSTGRES_DB")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

def create_database_and_user():
    conn = None
    cursor = None
    try:
        # Connect to PostgreSQL as the superuser
        conn = psycopg2.connect(
            dbname="postgres",
            user=POSTGRES_SUPERUSER,
            password=POSTGRES_SUPERPWD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Create new database user
        cursor.execute(f"SELECT 1 FROM pg_roles WHERE rolname=%s;", (NEW_DB_USER,))
        if not cursor.fetchone():
            cursor.execute(f"CREATE USER \"{NEW_DB_USER}\" WITH PASSWORD %s;", (NEW_DB_PASSWORD,))
            logger.info(f"User {NEW_DB_USER} created successfully.")
        else:
            logger.info(f"User {NEW_DB_USER} already exists.")

        # Create new database
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname=%s;", (NEW_DB_NAME,))
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {NEW_DB_NAME} OWNER \"{NEW_DB_USER}\";")
            logger.info(f"Database {NEW_DB_NAME} created successfully.")
        else:
            logger.info(f"Database {NEW_DB_NAME} already exists.")

        # Grant all privileges on the new database to the new user
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {NEW_DB_NAME} TO \"{NEW_DB_USER}\";")
        logger.info(f"Granted all privileges on database {NEW_DB_NAME} to user \"{NEW_DB_USER}\".")

    except Exception as e:
        logger.info(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database_and_user()
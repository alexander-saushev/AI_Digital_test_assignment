import os
import time
import logging
import pandas as pd
from sqlalchemy import create_engine, text, Table, Column, String, BigInteger, Float, MetaData, Text, inspect

logger = logging.getLogger(__name__)

# Config from environment variables
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


# === Database connection ===
def make_engine():
    conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn_str, pool_pre_ping=True)

# === Wait for the database to be ready ===
def wait_for_db(max_wait_s=60):
    start = time.time()
    while time.time() - start < max_wait_s:
        try:
            engine = make_engine()
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("DB is ready.")
            return engine
        except Exception as e:
            logger.warning(f"DB not ready yet: {e}")
            time.sleep(3)
    raise RuntimeError("Could not connect to DB within timeout.")


# === Create table if it does not exist ===
def ensure_table_exists(engine):
    metadata = MetaData()
    inspector = inspect(engine)

    if "countries" in inspector.get_table_names():
        logger.info("Table 'countries' already exists.")
        return

    # === Define countries table schema ===
    countries = Table(
        "countries",
        metadata,
        Column("name", String(100)),
        Column("population", BigInteger),
        Column("area", Float),
        Column("capital", String(100)),
        Column("flag_svg_url", Text),
        Column("tld", String(100)),
        Column("borders", String(100)),
        Column("timezones", String(100)),
        Column("languages", String(200)),
        Column("currencies", String(200)),
    )

    metadata.create_all(engine)
    logger.info("Table 'countries' created in database.")


# === Write data to Postgress ===
def write_to_db(df: pd.DataFrame, engine):
    ensure_table_exists(engine)

    try:
        df.to_sql("countries", engine, index=False, if_exists="replace")
        logger.info(f"Successfully updated table 'countries' with {len(df)} rows.")
    except Exception as e:
        logger.error(f"Failed to update data in 'countries': {e}")
        logger.warning("Table may be empty or contain previous data.")

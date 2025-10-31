import logging

from extract import get_session_with_retries, extract_countries
from transform import transform_countries
from load import wait_for_db, write_to_db

# === Logger configuration ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    session = get_session_with_retries()
    raw_data = extract_countries(session)

    df = transform_countries(raw_data)


    logger.info("Waiting for DB to be ready and writing data...")

    engine = wait_for_db()
    write_to_db(df, engine)
    logger.info("ETL finished successfully.")


if __name__ == "__main__":
    main()

from extract import extract
from Uncleaned_Data_validation import validate
from transform import transform
from load import load
import logging

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True
)

def main():
    logger = logging.getLogger("Main")
    logger.info("ETL Started")
    extract()

    validate()

    transform()

    load()
    logger.info("ETL Completed")

main()
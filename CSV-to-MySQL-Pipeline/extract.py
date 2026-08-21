import pandas as pd
import config
import logging
logger = logging.getLogger("Extract")
def extract():

   
   

    try:
        logger.info(f"Starting Extraction!")
        df=pd.read_csv(config.RAW_CSV)
        logger.info(f"{len(df)} rows extracted")
        return df
    except FileNotFoundError as e:
        logger.error(f"CSV File Not Found: {e}")
        raise
    except AttributeError as e:
        logger.error(e)
        raise
    except pd.errors.EmptyDataError as e:
        logger.error(f"CSV Empty: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        raise

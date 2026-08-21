import pandas as pd
import config
import logging
logger=logging.getLogger("Uncleaned_Data_validation")
df=pd.read_csv(config.RAW_CSV)


def validate():
    try:
            logger.info(f"Starting Validation of {len(df)} Records")
            rows=len(df)
            columns=len(df.columns)
            duplicate_orders=(df['Order_ID'].duplicated().sum())
            invalid_quantity=(df["Quantity"]<0).sum()
            missing_city=(df["Shipping_City"]).isna().sum()
            delivered_missing=(df["Customer_Rating"].isna() & (df["Order_Status"] == "Delivered")).sum()
            invalid_dates = df["Order_Date"].isna().sum()



            validation_report = {
                "Rows": len(df),
                "Columns": len(df.columns),
                "Duplicate Orders": duplicate_orders,
                "Invalid Quantity": invalid_quantity,
                "Missing Shipping City": missing_city,
                "Delivered Missing Rating": delivered_missing,
                "invalid_dates":invalid_dates
            }

            for check, value in validation_report.items():
                print(f"{check:<30}: {value}")
    except Exception as e:
         logger.error(f"Unexcpected Error {e}")
         

import pandas as pd
import config
import logging
logger=logging.getLogger("Transform")
def transform():
    try:
        
        df=pd.read_csv(config.RAW_CSV)
        
    
        logger.info("CSV Loaded Succesfully")

        logger.info(f"{len(df)} Rows ,{len(df.columns)} Columns Loaded!")

        # Drop Duplicates
        logger.info("Starting Transformation")
        logger.info(f"rows before removing duplicates:{len(df)}")

        df=df.drop_duplicates(keep="first")

        logger.info(f"rows after removing duplicates:{len(df)}")

        # Fillna Based on Business Rules
        logger.info(f"Nulls Before:{df['Discount_Percent'].isna().sum()}")
        df["Discount_Percent"]=df["Discount_Percent"].fillna(0)
        logger.info(f"Nulls After:{df['Discount_Percent'].isna().sum()}")

        # Change null of shipping city to Uknown

        logger.info(f"Before Changing: {df['Shipping_City'].isna().sum()} Nulls")


        df["Shipping_City"]=df["Shipping_City"].fillna("Unknown")

        logger.info(f"After Changing: {(df['Shipping_City']=='Unknown').sum()} Unknown")


        #Standardising Payments_Type Column
        payment_mapping = {
            "upi": "UPI",
            "u.p.i": "UPI",
            "credit card": "Credit Card",
            "credit_card": "Credit Card",
            "debit card": "Debit Card",
            "debit_card": "Debit Card",
            "netbanking":"Net Banking"
        }
        df["Payment_Method"]=(df["Payment_Method"].str.lower().replace(payment_mapping)) 

        df["Payment_Method"]=df["Payment_Method"].str.title()




    #Standardising Date
        df["Order_Date"]=pd.to_datetime(df["Order_Date"],format="mixed",errors="coerce")
        logger.info(f"Invalid Values: {df['Order_Date'].isna().sum()}")

        #Dealing with Negative Quantities create new seperate table for Negative Values for further investigation 
        invalid_quantity = df[df["Quantity"] <= 0]
        logger.info(f"Invalid Quantity: {len(df[df['Quantity'] <= 0])}")
        invalid_quantity.to_csv("rejected/invalid_quantity.csv",
                                index=False)
        #Dropping negative quantity rows in the main Dataset
        df = df[df["Quantity"] > 0]
        logger.info(f"Invalid Quantity After: {len(df[df['Quantity'] <= 0])}")


    #Standardising Country Column


        country_mapping = {
            "usa": "United States",
            "u.s.a": "United States",
            "us": "United States",
            "united states": "United States",

            "uk": "United Kingdom",
            "u.k.": "United Kingdom",
            "united kingdom": "United Kingdom",

            "uae": "United Arab Emirates",
            "u.a.e": "United Arab Emirates",

            "de": "Germany",
            "germany": "Germany",

            "ca": "Canada",
            "canada": "Canada",

            "au": "Australia",
            "australia": "Australia",

            "in": "India",
            "india": "India"
        }

        df["Country"]=df["Country"].str.lower().replace(country_mapping)

        print((df["Country"]).value_counts())
        logger.info("Saving processed CSV...")
        df.to_csv(
            "data/processed/ecommerce_clean.csv",
            index=False,
            date_format="%Y-%m-%d"
        )
        logger.info("Processed CSV saved successfully.")
        return df

    except AttributeError as e:
        logger.error(f"Input CSV not found: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        logger.error(f"CSV file is empty: {e}")
        raise
    except Exception as e:
        print(type(e))
        logger.critical(f"Unexpected error during transformation: {e}")
        raise

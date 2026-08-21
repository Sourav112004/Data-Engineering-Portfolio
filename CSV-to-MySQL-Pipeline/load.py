import pandas as pd
import mysql.connector
import config
import logging
df = pd.read_csv(config.PROCESSED_CSV)
logger=logging.getLogger('Load')

def load():
    try:
        
        conn = mysql.connector.connect(
        host=config.HOST,
        user=config.USER,
        password=config.PASSWORD,
        database=config.DATABASE
    )
        cursor=conn.cursor()
        cursor.execute("TRUNCATE TABLE ecommerce_orders")

        logger.info("Starting Load!")
        sql="""

        INSERT INTO ecommerce_orders (
        Order_ID,Customer_ID,Order_Date,Product_Category,Product_Name,Quantity,Unit_Price_USD,Discount_Percent,Payment_Method,Shipping_City,Country,Order_Status,Customer_Rating
        )
        VALUES(
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
        )


        """

        for index,rows in df.iterrows():
            raw_values=(
                rows["Order_ID"],
                rows["Customer_ID"],
                rows["Order_Date"],
                rows["Product_Category"],
                rows["Product_Name"],
                rows["Quantity"],
                rows["Unit_Price_USD"],
                rows["Discount_Percent"],
                rows["Payment_Method"],
                rows["Shipping_City"],
                rows["Country"],
                rows["Order_Status"],
                rows["Customer_Rating"]
            )
            new_values=[]
            for value in raw_values:
                if pd.isna(value):
                    new_values.append(None)
                else:
                    new_values.append(value)
            value=tuple(new_values)
            cursor.execute(sql,value)
        conn.commit()
        logger.info(f"Loaded Data Onto Mysql:{len(df)} Records Inserted")
        
     
    except Exception as e:
        logger.critical(f"MySQL Connection Failed! {e}")

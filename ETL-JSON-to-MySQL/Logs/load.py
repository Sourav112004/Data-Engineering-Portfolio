import pandas as pd
import mysql.connector
df=pd.read_json("Data/raw/processed/products_clean.json")
print(df[df["brand"].isna()])
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="product_etl"
)

cursor = conn.cursor()
print("Connected to MySQL!")
cursor.execute("TRUNCATE TABLE products")


sql="""
INSERT INTO products(
id, title, description, category, price, discountPercentage, rating, stock, brand, sku, weight,warrantyInformation,
 availabilityStatus, minimumOrderQuantity,width,height, depth, shipping_days, warranty_to_days,shippingInformation
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

for index,row in df.iterrows():
    raw_values=(
        row["id"],
        row["title"],
        row["description"],
        row["category"],
        row["price"],
        row["discountPercentage"],
        row["rating"],
        row["stock"],
        row["brand"],
        row["sku"],
        row["weight"],
        row["warrantyInformation"],
        row["availabilityStatus"],
        row["minimumOrderQuantity"],
        row["width"],
        row["height"],
        row["depth"],
        row["shipping_days"],
        row["warranty_to_days"],
        row["shippingInformation"]

    )
    new_values=[]
    for value in raw_values:
        if pd.isna(value):
            new_values.append(None)
        else:
            new_values.append(value)    
    values=tuple(new_values)


    cursor.execute(sql,values)


conn.commit()
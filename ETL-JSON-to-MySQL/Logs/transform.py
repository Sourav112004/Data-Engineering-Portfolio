import json
import pandas as pd
import re 

with open("data/raw/products.json", "r") as file:
        data = json.load(file)
        print("JSON File Loaded Succesfully")

products = data
df=pd.DataFrame(products)
print(df.info())


#Columns to drop
columns_to_drop=[
    "images",
    "thumbnail",
    "meta",
    "reviews",
    "tags",
    "returnPolicy"

      
]

df=df.drop(columns=columns_to_drop)


print(df.columns)

df["width"]=df["dimensions"].apply(
        lambda x: x.get("width")
)



df['height']=df['dimensions'].apply(

        lambda x:x.get("height")
)



df['depth']=df['dimensions'].apply(

        lambda x:x.get("depth")
)
print(df.columns)

#Function and regex to implement business data extraction of shipping date 
def shipping_to_days(text) :
        text = text.lower()
        if "overnight" in text:
                return 1


        if "week" in text:
                weeks=re.findall(r"\d+",text)
                return int(weeks[0])*7

        if "business days" in text:
                days=re.findall(r"\d+",text)
                return int(days[1])
        if "month" in text:
                months=re.findall(r"\d+",text)
                return int(months[0])*30
        
        return None
df["shipping_days"] = df["shippingInformation"].apply(shipping_to_days)

print(df["shipping_days"])


print(df.head)
#Dropping Dimension Column
df=df.drop(columns="dimensions")



def warranty_to_days(text):
        text=text.lower()
        if "week" in text :
                week=re.findall(r"\d+",text)
                return int(week[0])*7

        if "month" in text:
                month=re.findall(r"\d+",text)
                return int(month[0])*30
        
        if "year" in text:
                year=re.findall(r"\d+",text)
                return int(year[0])*365

        if "no warranty" in text:
                return 0
        if "lifetime" in text:
                return None

        return None

df["warranty_to_days"] = df["warrantyInformation"].apply(warranty_to_days)       

print(df["warranty_to_days"])


df.to_json(
    "data/raw/processed/products_clean.json",
    orient="records",
    indent=4
)


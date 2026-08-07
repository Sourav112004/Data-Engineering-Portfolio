import requests
import json

url = "https://dummyjson.com/products"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()
    total=data["total"]
    all_products=[]
    for skip in range(0,total,30):
        url=f"https://dummyjson.com/products?limit=30&skip={skip}"
        response = requests.get(url)
        data = response.json()
        all_products.extend(data["products"])
    with open("data/raw/products.json", "w") as file:
        json.dump(all_products, file, indent=4)

    print("Raw JSON saved successfully!")

else:
    print("API request failed.")

print(f"Total Products Downloaded: {len(all_products)}")

import requests
import json
import pandas as pd

# Encode the search term for URL
from urllib.parse import quote

product_details = pd.DataFrame(columns=["Title", "Price", "availability", "MRP"])
url = "https://2.rome.api.flipkart.com/api/4/page/fetch"


search_term = "iphone" ## dynamic search term

encoded_search = quote(search_term)

page_uri = f"/search?q={encoded_search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"

for n in range(1, 5):
    payload = json.dumps({
    "pageUri": page_uri,
    "pageContext": {
        "fetchSeoData": True,
        "paginatedFetch": False,
        "pageNumber": n
    },
    "requestContext": {
        "type": "BROWSE_PAGE",
        "ssid": "",
        "sqid": ""
    }
})
    headers = {
    'Sec-Fetch-Site': 'same-site',
    'X-User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 FKUA/website/42/website/Desktop',
    
    }

    response = requests.post(url, headers=headers, data=payload)
    print(response.status_code)
    print("page no:",n)
    if response.status_code == 200:
        data = response.json()
        try:
            slots = data.get("RESPONSE", {}).get("slots", [])
            for slot in slots:
                widget = slot.get("widget", {})
                if widget.get("type") == "PRODUCT_SUMMARY":
                    products = widget.get("data", {}).get("products", [])
                    for product in products:
                        info = product.get("productInfo", {}).get("value", {})
                        title = info.get("titles", {}).get("title", "N/A")
                        price = info.get("pricing", {}).get("finalPrice", {}).get("value", "")
                        availability = info.get("availability", {}).get("displayState", "")
                        mrp_price = info.get("pricing", {}).get("mrp", {}).get("value", "")
                        # print(f"Title: {title} | Price: ₹{price}")
                        # print(f"Title: {title} | Price: {price} | Availability: {availability} | MRP: {mrp_price}")
                        product_details.loc[len(product_details)] = [title, price, availability, mrp_price]
        except Exception as e:
            print("Error while parsing data:", e)
    else:
        print("Failed to fetch data.")
print(product_details)    
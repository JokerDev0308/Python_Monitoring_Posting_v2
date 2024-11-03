# for all shops on amazon.

# import requests
# from bs4 import BeautifulSoup

# async def check_stock_amazon(product_url):
#         """Scrapes Amazon Japan for stock information."""
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#         try:
#             response = requests.get(product_url, headers=headers)
#             soup = BeautifulSoup(response.content, 'html.parser')
            
#             # Check availability
#             availability = soup.find(id='add-to-cart-button')
#             image_url = soup.find('img', {'id': 'landingImage'})['src']
       
#             if availability:
#                 sale = soup.find(class_="a-price-whole").get_text().strip()
#                 return {'status': "在庫あり", 'sale': sale, 'image_url': image_url}
#             else:
#                 return {'status': "在庫なし", 'sale': 0, 'image_url': image_url}
#         except Exception as e:
#             print(f"Error fetching product page: {e}")
#             return {'status': "Error", 'sale': 0, 'image_url': ""}


##### for only amazon products

import requests
from bs4 import BeautifulSoup

async def check_stock_amazon(product_url):
    """Scrapes Amazon Japan for stock information."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(product_url, headers=headers, timeout=200)
        # Uncomment if you want to check for successful request
        # response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Check availability
        availability = soup.find(id='add-to-cart-button')
        image_tag = soup.find('img', {'id': 'landingImage'})
        image_url = image_tag['src'] if image_tag else ""  # Handle case where image is not found

        if availability:
            market_tag = soup.find_all(class_="offer-display-feature-text")
            if len(market_tag) > 2 and all("amazon" in tag.get_text().strip().lower() for tag in market_tag[1:4]):
                sale_arr = soup.find_all(class_="a-price-whole")
                sale = sale_arr[0].get_text().strip() if sale_arr else "0"  # Handle case where price is not found

                return {'status': "在庫あり", 'sale': sale, 'image_url': image_url}
            else:
                return {'status': "在庫なし", 'sale': 0, 'image_url': image_url}
        else:
            return {'status': "在庫なし", 'sale': 0, 'image_url': image_url}
    
    except requests.RequestException as e:
        print(f"Error fetching product page: {e}")
        return {'status': "エラー", 'sale': 0, 'image_url': ""}

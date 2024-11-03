import asyncio
from PyQt5.QtCore import QThread, pyqtSignal
from amazon_scraper import check_stock_amazon
from sns_posting import post_to_sns
from utils import get_product_status_by_name, update_product_status
from datetime import datetime

class MonitorThread(QThread):
    update_product_name = pyqtSignal(str)
    update_sale = pyqtSignal(str)  # Change to str for price display
    update_status = pyqtSignal(str)
    update_progress = pyqtSignal(int)
    update_result = pyqtSignal(str)
    update_image = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, products, posting_X_flag):
        super().__init__()
        self.products = products
        self.monitoring = True
        self.current_index = 0  # Start monitoring from the beginning
        self.posting_X_flag = posting_X_flag
    
    async def monitor_products(self):
        total_products = len(self.products)
        
        for index in range(self.current_index, total_products):
            if not self.monitoring:
                break

            product = self.products[index]
            adds_title = product["title"]
            product_name = product["product_name"]
            description = product["description"]
            affiliate_link = product["affiliate_link"]
            product_url = product["product_url"]

            
            # Proceed with checking stock information
            stock_info = await check_stock_amazon(product_url)
            current_price = int(stock_info['sale'].replace(',', '')) if stock_info['sale'] else 0
            current_status = stock_info['status']
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            pre_data = get_product_status_by_name(product_name)
           # Check if pre_data is None and set default values
            if pre_data is None:
                pre_status = "Unknown"
                pre_posted_date = "Unknown"
            else:
                pre_status = pre_data.get("current_status", "Unknown")
                pre_posted_date = pre_data.get("postedDate", "Unknown")
            # print(product_name,pre_posted_date,pre_status)

            start_price = self.clean_price(product.get('start_price'))
            end_price = self.clean_price(product.get('end_price'))

            self.update_product_name.emit(product_name)
            self.update_sale.emit(f"{current_price} 円")  # Japanese yen
            self.update_status.emit(current_status)
            self.update_image.emit(stock_info.get('image_url', ""))
            self.update_progress.emit(int((index + 1) / total_products * 100))

            postedDate = pre_posted_date

            if current_status == '在庫あり' and pre_status != current_status:
                postedDate = current_time
                self.handle_in_stock(adds_title, product_name, current_price, start_price, end_price, description, affiliate_link, current_time)
            elif current_status == '在庫あり' and pre_status == current_status:
                self.update_result.emit(f"{pre_posted_date} {product_name} はすでに投稿されています")
            else:
                self.update_result.emit(f"{current_time} {product_name} は在庫切れです")

            # Prepare status data for saving
            status_data = {
                'product_name': product_name,
                'current_price': current_price,
                'current_status': current_status,
                'monitoredDate': current_time,
                'postedDate': postedDate
            }

            update_product_status(status_data)

            await asyncio.sleep(1)  # Simulate delay

        self.finished.emit()  # Emit finished when done

    def clean_price(self, price_str):
        """Convert price string to int, handling various formats."""
        if isinstance(price_str, str) and price_str not in (None, '', 'NaN'):
            return int(price_str.replace(',', ''))
        return None

    def handle_in_stock(self, adds_title, product_name, current_price, start_price, end_price, description, affiliate_link, current_time):
        """Handle actions for products that are in stock."""
        # Convert adds_title and description to strings before checking
        adds_title_str = str(adds_title) if adds_title is not None else ""
        description_str = str(description) if description is not None else ""

        message = f"{adds_title_str if adds_title_str.lower() != 'nan' else '💡在庫復活💡PR'}\n  {current_time}\n {product_name}\n {current_price}円\n {f'{description_str}\n' if description_str.lower() != 'nan' else ''}  {affiliate_link}"

        if start_price is not None and end_price is not None:
            if start_price <= current_price <= end_price:
                post_to_sns(message,self.posting_X_flag)
                self.update_result.emit(f"{current_time} : {product_name} は在庫ありで価格は {current_price}円、範囲 {start_price}~{end_price}円 ですので、投稿しました")
            else:
                self.update_result.emit(f"{current_time} : {product_name} は在庫ありですが価格は {current_price}円で範囲 {start_price}~{end_price}円 を超えていますので、投稿しません")
        elif start_price is not None:
            if start_price <= current_price:
                post_to_sns(message,self.posting_X_flag)
                self.update_result.emit(f"{current_time} : {product_name} は在庫ありで価格は {current_price}円が {start_price}円 以上ですので、投稿しました")
            else:
                self.update_result.emit(f"{current_time} : {product_name} は在庫ありですが価格は {current_price}円で {start_price}円 未満ですので、投稿しません")
        elif end_price is not None:
            if current_price <= end_price:
                post_to_sns(message,self.posting_X_flag)
                self.update_result.emit(f"{current_time} : {product_name} は在庫ありで価格は {current_price}円が {end_price}円 以下ですので、投稿しました")
            else:
                self.update_result.emit(f"{current_time} : {product_name} は在庫ありですが価格は {current_price}円で {end_price}円 を超えていますので、投稿しません")
        else:
            post_to_sns(message,self.posting_X_flag)
            self.update_result.emit(f"{current_time} : {product_name} は在庫ありで価格は {current_price}円ですので、投稿しました")


    def run(self):
        asyncio.run(self.monitor_products())  # Run the async function in the thread


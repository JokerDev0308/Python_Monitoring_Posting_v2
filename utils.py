import json
import os
import pandas as pd
from datetime import datetime

SETTINGS_FILE = 'settings.json'
LOG_FILE = "post_log.txt"
PRODUCT_LIST_FILE = 'product_list.xlsx'
STATUS_FILE = 'product_status.json'

def log_post_status(message):
    """Logs the post status with a timestamp."""
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        print(f"Error logging message: {e}")

def load_product_list():
    """Loads the product list from an Excel file."""
    try:
        df = pd.read_excel(PRODUCT_LIST_FILE, sheet_name='product_list')
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error loading product list: {e}")
        log_post_status(f"Error loading product list: {e}")
        return []

def load_settings():
    """Loads settings from the Excel file."""
    try:
        df = pd.read_excel(PRODUCT_LIST_FILE, sheet_name='settings')
        return df.to_dict(orient='records')[0]
    except Exception as e:
        print(f"Error loading settings: {e}")
        log_post_status(f"Error loading settings: {e}")
        return {}

def save_settings(settings):
    """Saves settings to the Excel file."""
    try:
        df = pd.DataFrame([settings])
        with pd.ExcelWriter(PRODUCT_LIST_FILE, engine='openpyxl', mode='a') as writer:
            df.to_excel(writer, sheet_name='settings', index=False)
    except Exception as e:
        print(f"Error saving settings: {e}")
        log_post_status(f"Error saving settings: {e}")

def is_within_notification_time():
    """Check if current time is within the notification window."""
    settings = load_settings()
    current_time = datetime.now().time()
    start_time = datetime.strptime(settings['notification_start_time'], "%H:%M").time()
    end_time = datetime.strptime(settings['notification_end_time'], "%H:%M").time()
    
    return start_time <= current_time <= end_time

def load_product_status():
    """Load product status from a JSON file."""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def get_product_status_by_name(product_name):
    """Retrieve a product by its name from the product status list."""
    status_list = load_product_status()
    for product in status_list:
        if product['product_name'] == product_name:
            return product
    return None  # Return None if the product is not found

def save_product_status(products):
    """Save product status to a JSON file."""
    try:
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving product status: {e}")
        log_post_status(f"Error saving product status: {e}")

def update_product_status(data):
    """Update product status in the JSON file."""
    statuses = load_product_status()

    for idx, item in enumerate(statuses):
        if item['product_name'] == data['product_name']:
            statuses[idx] = data
            log_post_status(f"Updated status for {data['product_name']}")
            break
    else:
        statuses.append(data)
        log_post_status(f"Added new product status for {data['product_name']}")

    save_product_status(statuses)

import requests
import json
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logging.info("MonitorMate started.")

def load_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config['url_to_monitor']

def check_website_status(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            log_status(f"[{datetime.now()}] {url} is UP")
        else:
            log_status(f"[{datetime.now()}] {url} returned status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        log_status(f"[{datetime.now()}]  {url} is DOWN. Error: {e}")

def log_status(status_message):
    with open("logs/alert_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {status_message}\n")
    while True:
        print("Checking website status...")
        time.sleep(2)

if __name__ == "__main__":
    url_to_monitor = load_config()  # Load URL from config
    check_website_status(url_to_monitor)

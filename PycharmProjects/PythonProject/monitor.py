import requests
import json
import time
import logging
import sqlite3
from datetime import datetime
import os

pwd = "/users/ramyamunusamy/PycharmProjects/PythonProject/"
configPath = os.path.join(pwd, 'config.json')

logging.basicConfig(level=logging.INFO)
logging.info("MonitorMate started.")

def load_config():
    with open(configPath, "r") as config_file:
        config = json.load(config_file)
    return config['url_to_monitor']

def monitor_url(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        response_time = time.time() - start_time
        status = 'Up' if response.status_code == 200 else 'Down'
    except requests.exceptions.RequestException:
        status = 'Down'
        response_time = 0.0

    log_status(f"[{datetime.now()}]  {url} is {status}. Response time {response_time}")
    log_to_database(url, status, response_time)

def log_to_database(url, status, response_time):
    conn = sqlite3.connect('monitoring.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO monitor_data (url, status, response_time)
                   VALUES (?, ?, ?)''', (url, status, response_time))
    conn.commit()
    conn.close()

def log_status(status_message):
    with open(pwd+"/logs/alert_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {status_message}\n")

if __name__ == "__main__":
    url_to_monitor = load_config()  # Load URL from config
    for url in url_to_monitor:
        monitor_url(url)

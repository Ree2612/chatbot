import requests
import csv
from datetime import datetime
import os

LOG_FILE = "logs.csv"

# Function to get user's public IP
def get_public_ip():
    try:
        ip = requests.get("https://api64.ipify.org").text
        return ip
    except:
        return "127.0.0.1"

# Function to get geolocation from IP
def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        return {
            "ip": ip,
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country"),
            "countryCode": data.get("countryCode"),
            "isp": data.get("isp"),
            "lat": data.get("lat"),
            "lon": data.get("lon")
        }
    except:
        return {
            "ip": ip, "city": None, "region": None,
            "country": None, "countryCode": None,
            "isp": None, "lat": None, "lon": None
        }

# Function to log threat
def log_threat(ip, geo, query, is_threat, terms):
    log_row = [
        datetime.now(), ip, geo['city'], geo['region'], geo['country'],
        geo['countryCode'], geo['lat'], geo['lon'], geo['isp'], query,
        is_threat, "|".join(terms)
    ]

    # Ensure folder exists (only if a directory is specified)
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(log_row)


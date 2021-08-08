"""

This script continuously checks if the ISS is overhead the
users current location, and if it is, sends an email to the user
notifying them.

This script requires that 'requests', 'smtplib', 'python-dotenv' be installed within the Python
environment you are running this script in.

"""

import requests
import datetime as dt
import smtplib
import time
from dotenv import load_dotenv
import os

load_dotenv(".env")
GMAIL_USERNAME = os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
MY_LAT = float(os.getenv("MY_LAT"))
MY_LONG = float(os.getenv("MY_LONG"))
HOTMAIL_USERNAME = os.getenv("HOTMAIL_USERNAME")

# websiteforlookingatlatlongonmap https://www.latlong.net/Show-Latitude-Longitude.html
# API Endpoint for JSON data http://open-notify.org/Open-Notify-API/ISS-Location-Now/

# obtaining the position of the iss


def is_iss_overhead():
    """Sends a request to an api that returns the location of the iss station
    """

    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data['iss_position']['longitude'])
    iss_latitude = float(data['iss_position']['latitude'])
    if MY_LAT + 5 >= iss_latitude >= MY_LAT - 5 and MY_LONG + 5 >= iss_longitude >= MY_LONG - 5:
        return True
# Sunrise and sunset times


def is_nighttime():
    """Sends a request to obtain the sunset and sunrise times for the
    users current location"""

    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted':0
    }
    response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']
    sunrise_hour = int(sunrise.split('T')[1].split(':')[0])
    sunset_hour = int(sunset.split('T')[1].split(':')[0])
    time_now = dt.datetime.utcnow()
    time_now_hour = time_now.hour
    if sunrise_hour >= time_now_hour >= 0 or sunset_hour <= time_now_hour <= 23:
        return True
# If the ISS is close to my current location [+- 5 lat and long] and it is dark
# send me an email to tell me to look up
# BONUS: Run the code every 60 seconds


while True:
    time.sleep(60)
    if is_nighttime() and is_iss_overhead(): # change the or back to and after!@!@!@!
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=GMAIL_USERNAME, password=GMAIL_PASSWORD)
            connection.sendmail(from_addr=GMAIL_USERNAME, to_addrs=HOTMAIL_USERNAME, msg='Subject:LOOK UP\n\nTHE ISS IS'
                                                                                         'VISIBLE!!!!')
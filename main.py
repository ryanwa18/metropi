import requests
import os
import digitalio
import busio
import board
import time
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from dotenv import load_dotenv
from display_metro_graphics import Metro_Graphics

## Load the env variable 
load_dotenv()

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

## Station code can be set to 'All' to get all the stations or 
## a specific station code such as B03
station_code = 'B03'

api_key = os.getenv('METRO_API_KEY')
api_url = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{}'.format(station_code)

request_headers = {'api_key': api_key}

display = Adafruit_SSD1675(   # Older eInk Bonnet
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)

display.rotation = 1
gfx = Metro_Graphics(display)
refresh_display = None

while True:
    if (not refresh_display) or (time.monotonic() - refresh_display) > 60:
        request = requests.get(api_url, request_headers).json()
        gfx.display_metro(request)
        refresh_display = time.monotonic()
    
    gfx.update_time()
    time.sleep(60)

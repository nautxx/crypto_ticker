import requests
import json
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, ATARI_FONT, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, SPECCY_FONT, TINY_FONT
import time
from datetime import datetime, timedelta


coin = "BTC"    #Cryptocoin Ticker Symbol: BTC, DOGE, ETH, etc.
currency = "USD"    #Currency Abbreviation: USD, AUD, DOGE, ETH, etc.

api_key = "8ec5a22972553ddb1eff5a049dd2947b43e0d00237c0ffaae719a6e9a2eef3b8"    #None if no api_key
link = "https://min-api.cryptocompare.com/data/pricemulti?fsyms={0}&tsyms={1}".format(coin, currency)
api_request_frequency = 300   #in seconds

if api_key is not None:
    link += "&api_key=" + api_key

while True:
    page = requests.get(link)
    page_parsed = json.loads(page.text)

    price = page_parsed[coin][currency]
    price_format = "{:,}".format(price) #adds commas for readability

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, rotate=2, contrast=1)

    message = coin.lower() + "-" + currency.lower() + ": $" + str(price_format)   
    
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(message)
    for x in range(3):
        show_message(device, message, y_offset=0, fill="white", font=proportional(TINY_FONT), scroll_delay=0.06)
    
    update_timestamp = (datetime.now() + timedelta(seconds=api_request_frequency)).strftime("%Y-%m-%d %H:%M:%S")
    print("next update: ", update_timestamp)
    time.sleep(api_request_frequency)   #adds time delay in (s, seconds) before looping
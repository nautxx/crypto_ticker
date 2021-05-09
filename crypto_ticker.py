import requests
import json
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, ATARI_FONT, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, SPECCY_FONT, TINY_FONT
import time
from datetime import datetime, timedelta
from config import api_db, crypto_currency

crypto = {}

def get_crypto(coin="BTC", currency="USD"): #Cryptocoin Ticker Symbol: BTC, DOGE, ETH, etc.
    crypto[0] = coin
    crypto[1] = currency 

def get_api_link(key=None):
    link = "https://min-api.cryptocompare.com/data/pricemulti?fsyms={0}&tsyms={1}".format(crypto[0], crypto[1])
    if key is not None:
        link += "&api_key=" + key
        return link
    return link

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
    
    update_timestamp = (datetime.now() + timedelta(seconds=api_key['frequency'])).strftime("%Y-%m-%d %H:%M:%S")
    print("next update: ", update_timestamp)
    time.sleep(api_key['frequency'])   #adds time delay in (s, seconds) before looping
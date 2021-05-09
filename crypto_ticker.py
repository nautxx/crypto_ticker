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

def parse_the_link():
    page = requests.get(get_api_link(api_db['key']))
    page_parsed = json.loads(page.text)
    return page_parsed

def get_current_timestamp():
    return datetime.now().strftime("%Y.%m.%d %H:%M:%S")

def get_next_timestamp():
    timestamp = (datetime.now() + timedelta(seconds=api_db['freq'])).strftime("%Y.%m.%d %H:%M")
    return timestamp

def get_prices(link):
    prices = ""
    for coin in link:
        for currency in link[coin]:
            price = link[coin][currency]
            price_formatted = "{:,}".format(price)
            if coin != currency:
                prices += "{0}-{1}: {2}".format(coin, currency, price_formatted).lower() + '\t' + get_current_timestamp() + "\n"
    return prices

def get_prices_led(link, spacing=1):
    prices = ""
    spaces = ""
    for space in range(spacing):
        spaces += " "
    for coin in link:
        for currency in link[coin]:
            price = link[coin][currency]
            price_formatted = "{:,}".format(price)
            if coin != currency:
                prices += "{0}-{1}: {2}{3}".format(coin, currency, price_formatted, spaces).lower()
    return prices

def display_ticker(set_range=1):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, rotate=2, contrast=1)

    for tick in range(set_range):
        show_message(device, ticker_message, y_offset=0, fill="white", font=proportional(TINY_FONT), scroll_delay=0.06)

get_crypto(crypto_currency['coin'], crypto_currency['currency'])

while True: # loop to infiniti
    parsed_link = parse_the_link()
    ticker_message = get_prices_led(parsed_link, 6)
    terminal_message = get_prices(parsed_link)
    
    print("\n" + terminal_message)
    print("Next Update: ".lower() , get_next_timestamp())

    display_ticker()
    time.sleep(api_db['freq'])   # adds time delay in (s, seconds) before looping
import requests
import json
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, ATARI_FONT, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, SPECCY_FONT, TINY_FONT

coin = "BTC"    #BTC, DOGE, ETH, etc.
currency = "USD"    #USD, AUD, DOGE, ETH, etc.

while True:

    page = requests.get("https://min-api.cryptocompare.com/data/pricemulti?fsyms={0}&tsyms={1}".format(coin, currency))
    page_parsed = json.loads(page.text)

    price = page_parsed[coin][currency]
    price_format = "{:,}".format(price)

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, rotate=2, contrast=1)

    message = coin.lower() + "-" + currency.lower() + ": $" + str(price_format)

    show_message(device, message, y_offset=0, fill="white", font=proportional(TINY_FONT), scroll_delay=0.06)
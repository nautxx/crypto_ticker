import platform
import click
import requests
import json
import time
from datetime import datetime, timedelta
from config import config

system = platform.system() not in ['Darwin', 'Java', 'Windows']
if system:  #skip luma load when using mac or windows operating systems
    from luma.led_matrix.device import max7219
    from luma.core.interface.serial import spi, noop
    from luma.core.legacy import text, show_message
    from luma.core.legacy.font import proportional, ATARI_FONT, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, SPECCY_FONT, TINY_FONT

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, rotate=2, contrast=1)

class User(object): #initialize user data
    def __init__(self, coin=None, currency=None, apikey=None, message=None):
        self.coin = coin
        self.currency = currency
        self.apikey = apikey

@click.group()
@click.option('--coin', default='BTC', help='Crypto ticker symbol. Multiple ticker symbols separate with comma')
@click.option('--currency', default='USD', help='Currency. Multiple currencies separate with comma')
@click.option('--apikey', help='Enter API key from cryptocompare.com')
@click.pass_context
def main(ctx, coin, currency, api): #user stored values entered in cli
    ctx.obj = User(coin, currency, apikey)

@click.pass_obj
def parse_the_link(ctx):
    link = config['link'].format(ctx.coin, ctx.currency)
    if ctx.apikey is not None:
        link += "&api_key=" + ctx.apikey
    page = requests.get(link)
    page_parsed = json.loads(page.text)
    return page_parsed

def get_current_timestamp():
    return datetime.now().strftime("%Y.%m.%d %H:%M:%S")

def get_next_timestamp():
    time_offset = len(ticker_message)
    timestamp = (datetime.now() + timedelta(seconds=api_db['freq'] + time_offset)).strftime("%Y.%m.%d %H:%M")
    return timestamp

def get_prices(link, spacing=1):
    prices, prices_display, spaces = '','',''

    for space in range(spacing):
        spaces += " "

    for coin in link:
        for currency in link[coin]:
            price = link[coin][currency]
            price_formatted = "{:,}".format(price)
            if coin != currency:
                prices += "{0}-{1}: {2}".format(coin, currency, price_formatted).lower() + '\t' + get_current_timestamp() + "\n"
                prices_display += "{0}-{1}: {2}{3}".format(coin, currency, price_formatted, spaces).lower()

    return prices, prices_display

def ticker_display(set_range=1):
    for tick in range(set_range):
        show_message(device, ticker_message, y_offset=0, fill='white', font=proportional(TINY_FONT), scroll_delay=0.06)

@main.command()
@click.pass_obj
def cryptoticker_endless(ctx):  # loop to infiniti
    while True:
            parsed_link = parse_the_link()
            terminal_message, ticker_message = get_prices(parsed_link)
            
            print("\n" + terminal_message)
            print("Next Update: ".lower(), get_next_timestamp())
            if system:
                ticker_display()
            time.sleep(config['frequency'])   # adds time delay in (s, seconds) before looping

if __name__ == '__main__':
    main()
import platform
import click
import requests
import json
import time
from datetime import datetime, timedelta
from config import config
from pathlib import Path
from color import Color

system = platform.system() not in ['Darwin', 'Java', 'Windows']
if system:  #skip luma load when using mac or windows operating systems
    from luma.core.interface.serial import spi, noop
    from luma.core.render import canvas
    from luma.core.legacy import text, show_message
    from luma.core.legacy.font import proportional, ATARI_FONT, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, SPECCY_FONT, TINY_FONT
    from luma.led_matrix.device import max7219

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, rotate=2, contrast=1)

class User(object): #initialize user data
    def __init__(self, coin=None, currency=None, apikey=None, message=None, count=1):
        self.coin = coin
        self.currency = currency
        self.apikey = apikey
        self.message = message
        self.count = count

@click.group()
@click.option('--coin', default='BTC', help='Crypto ticker symbol. Multiple ticker symbols separate with comma')
@click.option('--currency', default='USD', help='Currency. Multiple currencies separate with comma')
@click.option('--apikey', default=None, help='Enter API key from cryptocompare.com')
@click.option('--message', prompt='Your message', help='Enter message to display for message_bar')
@click.option('--count', default=1, help='Number of times to display')
@click.pass_context
def main(ctx, coin, currency, apikey, message, count): #user stored values entered in cli
    ctx.obj = User(coin, currency, apikey, message, count)

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
    timestamp = (datetime.now() + timedelta(seconds=config['frequency'])).strftime("%Y.%m.%d %H:%M")
    return timestamp

def get_prices(link, spacing=1):
    prices, prices_display, spaces = '','',''

    for space in range(spacing):
        spaces += ' '

    for coin in link:
        for currency in link[coin]:
            price = link[coin][currency]
            price_formatted = "{:,}".format(price)
            if coin != currency:
                prices += "{0}-{1}: {2}".format(coin, currency, price_formatted).lower() + '\t' + get_current_timestamp() + "\n"
                prices_display += "{0}-{1}: {2}{3}".format(coin, currency, price_formatted, spaces).lower()

    return prices, prices_display

def get_data(link, spacing=1):
    output, output_display = '', ''
    for coin in link['RAW']:
        for currency in link['RAW'][coin]:
            if coin != currency:
                for category in link['RAW'][coin][currency]:
                    value = link['RAW'][coin][currency][category]   
                    currency_symbol = link['RAW'][coin][currency]['TOSYMBOL']
                    price = link['RAW'][coin][currency]['PRICE']
                    last_update = (datetime.fromtimestamp(link['RAW'][coin][currency]['LASTUPDATE']) - timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
                    twenty_four_hour_low = link['RAW'][coin][currency]['LOW24HOUR']
                    twenty_four_hour_high = link['RAW'][coin][currency]['HIGH24HOUR']
                    twenty_four_hour = link['RAW'][coin][currency]['CHANGE24HOUR']
                    twenty_four_hour_pct = link['RAW'][coin][currency]['CHANGEPCT24HOUR']
                    hour = link['RAW'][coin][currency]['CHANGEHOUR']
                    hour_pct = link['RAW'][coin][currency]['CHANGEPCTHOUR']
                    supply = link['RAW'][coin][currency]['SUPPLY']

                    if price <= 1 and price >= -1:
                        price_format = '{0:,.8f}'.format(float(price))
                    else:
                        price_format = '{0:,.2f}'.format(float(price))

                    if twenty_four_hour <= 1 and twenty_four_hour >=-1:
                        twenty_four_hour_format = '{0:+,.8f}'.format(float(twenty_four_hour))
                    else:
                        twenty_four_hour_format = '{0:+,.2f}'.format(float(twenty_four_hour))

                    if twenty_four_hour_pct <= 1 and twenty_four_hour_pct >=-1:
                        twenty_four_hour_pct_format = '{0:+,.2f}'.format(float(twenty_four_hour_pct))
                    else:
                        twenty_four_hour_pct_format = '{0:+,.2f}'.format(float(twenty_four_hour_pct))

                    if float(twenty_four_hour_pct) >= 0:
                        twenty_four_hour_color = Color.f.green
                    else:
                        twenty_four_hour_color = Color.f.red

                    if hour <= 1 and hour >=-1:
                        hour_format = '{0:+,.8f}'.format(float(hour))
                    else:
                        hour_format = '{0:+,.2f}'.format(float(hour))

                    if hour_pct <= 1 and hour_pct >=-1:
                        hour_pct_format = '{0:+,.2f}'.format(float(hour_pct))
                    else:
                        hour_pct_format = '{0:+,.2f}'.format(float(hour_pct))
                        
                    if float(hour_pct) >= 0:
                        hour_color = Color.f.green
                    else:
                        hour_color = Color.f.red

            output += str(coin + '-' + currency_symbol).ljust(12,' ') \
                    + str(price_format).rjust(12,' ') + '\t' + twenty_four_hour_color \
                    + str(twenty_four_hour_format).rjust(12,' ') + '\t'\
                    + str('(' + twenty_four_hour_pct_format + '%)').rjust(10,' ') + hour_color \
                    + str(hour_format).rjust(12,' ') + '\t' \
                    + str('(' + hour_pct_format + '%)').rjust(10,' ') + Color.end \
                    + str(last_update + '\n').rjust(24,' ')

            output_display += str(str(coin + '-' + currency_symbol + ": ")).lower() + str(price_format) \
                    + str(' ' + hour_format + '    ')

    return output, output_display

def logger(message):
    path = Path(__file__).parent.absolute()
    file = open(str(path) + "/message_log.txt", "a")
    file.write("\n" + get_current_timestamp() + ": " + message)
    file.close

@main.command()
@click.pass_obj
def cryptoticker_endless(ctx):  # loop to infiniti
    while True:
        parsed_link = parse_the_link()
        terminal_message, ticker_message = get_data(parsed_link)
        print('\n' + "           \t   Price                24hr           pct         1hr         pct            Last update" + '\n' + terminal_message)
        print("Next Update: ".lower(), get_next_timestamp())
        print("Press 'Ctrl + C' to exit")
        if system:
            for tick in range(ctx.count):
                show_message(device, message, y_offset=0, fill='white', font=proportional(TINY_FONT), scroll_delay=0.06)
        time.sleep(config['frequency'])   # loop time delay in (s, seconds)

@main.command()
@click.pass_obj
def messagebar_scrolling(ctx):
    logger(ctx.message)
    print('"' + ctx.message + '" sent successfully.')

    if system:
        for letter in range(ctx.count):
            show_message(device, ctx.message, fill='white', font=proportional(TINY_FONT), scroll_delay=0.06)

@main.command()
@click.pass_obj
def messagebar_static(ctx):
    logger(ctx.message)
    print('"' + ctx.message + '" sent successfully.')

    if system:
        with canvas(device) as draw:
            text(draw, (0, 0), ctx.message, fill='white', font=proportional(TINY_FONT))
        time.sleep(ctx.count)  #time in (s, seconds) to display the static text


if __name__ == '__main__':
    main()
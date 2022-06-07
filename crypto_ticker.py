import platform
import click
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from ticker_search import TickerSearch
from messagebar import MessageBar

# skips luma libraries from loading when using mac or windows operating systems
system = platform.system() not in ['Darwin', 'Java', 'Windows']
if system:
    from luma.core.interface.serial import spi, noop
    from luma.core.render import canvas
    from luma.core.legacy import text, show_message
    from luma.core.legacy.font import proportional, ATARI_FONT, CP437_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT, SPECCY_FONT, TINY_FONT
    from luma.led_matrix.device import max7219

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(
        serial, 
        cascaded=4, 
        block_orientation=-90, 
        rotate=2, 
        contrast=1
    )


DELAY = 300


def get_current_timestamp():
    timestamp = datetime.now()
    timestamp_formatted = timestamp.strftime("%Y.%m.%d %H:%M:%S")
    return timestamp

def get_next_update_timestamp():
    next_time_stamp = (datetime.now() + timedelta(seconds=DELAY))
    next_time_stamp_formatted = next_time_stamp.strftime("%Y.%m.%d %H:%M:%S")
    return next_time_stamp

    
class User(object): 
    """Initializes user data input from command line."""
    def __init__(self, coin=None, currency=None, apikey=None, message=None, count=1):
        self.coin = coin
        self.currency = currency
        self.apikey = apikey
        self.message = message
        self.count = count

@click.group()
@click.option(
    '--coin', 
    default='BTC', 
    help='Crypto ticker symbol. Multiple ticker symbols separate with comma'
)
@click.option(
    '--currency', 
    default='USD', 
    help='Currency. Multiple currencies separate with comma'
)
@click.option(
    '--apikey', 
    default=None, 
    help='Enter API key from cryptocompare.com'
)
@click.option(
    '--message', 
    default=None, 
    help='Enter message to display for message_bar'
)
@click.option(
    '--count', 
    default=1, 
    help='Scrolling: Number of times to loop display. Static: Time in seconds to display'
)

@click.pass_context
# user stored values entered in cli
def main(ctx, coin, currency, apikey, message, count):
    ctx.obj = User(coin, currency, apikey, message, count)


@main.command()
@click.pass_obj
def cryptoticker_endless(ctx):
    """
    Ticker terminal display and scrolling ticker bar will display indefinitely.
    """
    ticker_search = TickerSearch()
    while True:
        terminal_message, ticker_message = ticker_search.compare_crypto(ctx.apikey, ctx.coin, ctx.currency)
        header = '\n' + "           \t   Price                24hr           pct         1hr         pct            Last update" + '\n'
        footer = "Next Update: ".lower() + str(get_next_update_timestamp())\
            + "\nPress 'Ctrl + C' to exit"
        print(header + terminal_message)
        print(footer)
        if system:
            for tick in range(ctx.count):
                show_message(
                    device,
                    ticker_message,
                    y_offset=0,
                    fill='white',
                    font=proportional(TINY_FONT),
                    scroll_delay=0.06
                )
        # loop time delay in (s, seconds)
        time.sleep(DELAY)


@main.command()
@click.pass_obj
def messagebar_scrolling(ctx):
    message_bar = MessageBar()
    if ctx.message is None:
        ctx.message = input("Your message: ")
    message_bar.logger(str(get_current_timestamp()), ctx.message, "scrolling")

    if system:
        label = 'Displaying'
        fill_char = click.style('#', fg='green')
        empty_char = click.style('-', fg='white', dim=True)
        length = 100

        print(f'Message "{ctx.message}" has been sent successfully.')  
        with click.progressbar(
            label=label, 
            length=length, 
            fill_char=fill_char, 
            empty_char=empty_char, 
            show_eta=False
        ) as bar:
            bar.update(0)
            for letter in range(ctx.count):
                show_message(
                    device, 
                    ctx.message, 
                    fill='white', 
                    font=proportional(TINY_FONT), 
                    scroll_delay=0.06
                )
                bar.update(length / ctx.count)
    else:
        print(f'Message "{ctx.message}" has been logged successfully.')        


@main.command()
@click.pass_obj
def messagebar_static(ctx):
    if ctx.message is None:
        ctx.message = input("Your message: ")
    message_bar.logger(str(get_current_timestamp()), ctx.message, "static")

    if system:
        with canvas(device) as draw:
            text(
                draw, 
                (0, 0), 
                tx.message,
                fill='white', 
                font=proportional(TINY_FONT)
            )
        
        refresh = 10
        iterable = range(ctx.count * refresh)
        label = 'Displaying'
        fill_char = click.style('#', fg='green')
        empty_char = click.style('-', fg='white', dim=True)

        print(f'Message "{ctx.message}" has been sent successfully.')   
        with click.progressbar(
            iterable = iterable,
            label = label,
            fill_char = fill_char,
            empty_char = empty_char
        ) as bar:
            for tick in bar:                
                time.sleep(1 / refresh)
    else:
        print(f'Message "{ctx.message}" has been logged successfully.')   


if __name__ == '__main__':
    main()
import requests
from datetime import datetime, timedelta
from color import Color
from ticker_data import TickerData
import os
from dotenv import load_dotenv  # pip install python-dotenv
import pandas as pd


API_KEY = os.environ.get("API_KEY")
CRYPTOCOMPARE_ENDPOINT = "https://min-api.cryptocompare.com/data/pricemultifull"


class TickerSearch:
    def __init__(self):
        pass


    def compare_crypto(self, api_key, coin, currency):
        output, output_display = "", ""

        headers = {"api_key": API_KEY}
        query = {"fsyms": coin, "tsyms": currency}
        response = requests.get(
            url=f"{CRYPTOCOMPARE_ENDPOINT}",
            headers=headers,
            params=query
        )
        data = response.json()
        data_df = pd.DataFrame(data)

        for coin in data['RAW']:
            for currency in data['RAW'][coin]:
                if coin != currency:
                    for category in data['RAW'][coin][currency]:
                        ticker_data = TickerData(
                            currency_symbol=data['RAW'][coin][currency]['TOSYMBOL'], 
                            price=data['RAW'][coin][currency]['PRICE'], 
                            last_update=(datetime.fromtimestamp(data['RAW'][coin][currency]['LASTUPDATE']) - timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S'), 
                            twenty_four_hour_low=data['RAW'][coin][currency]['LOW24HOUR'], 
                            twenty_four_hour_high=data['RAW'][coin][currency]['HIGH24HOUR'], 
                            twenty_four_hour_change=data['RAW'][coin][currency]['CHANGE24HOUR'], 
                            twenty_four_hour_change_pct=data['RAW'][coin][currency]['CHANGEPCT24HOUR'], 
                            hour_change=data['RAW'][coin][currency]['CHANGEHOUR'], 
                            hour_change_pct=data['RAW'][coin][currency]['CHANGEPCTHOUR'], 
                            supply=data['RAW'][coin][currency]['SUPPLY']
                        )

                        if ticker_data.price <= 1 and ticker_data.price >= -1:
                            price_format = '{0:,.8f}'.format(float(ticker_data.price))
                        else:
                            price_format = '{0:,.2f}'.format(float(ticker_data.price))

                        if ticker_data.twenty_four_hour_change <= 1 and ticker_data.twenty_four_hour_change >=-1:
                            twenty_four_hour_format = '{0:,.8f}'.format(abs(float(ticker_data.twenty_four_hour_change)))
                            if float(ticker_data.twenty_four_hour_change_pct) < 0:
                                twenty_four_hour_format = "▼" + str(twenty_four_hour_format)
                            else:
                                twenty_four_hour_format = "▲" + str(twenty_four_hour_format)
                        else:
                            twenty_four_hour_format = '{0:,.2f}'.format(abs(float(ticker_data.twenty_four_hour_change)))
                            if float(ticker_data.twenty_four_hour_change_pct) < 0:
                                twenty_four_hour_format = "▼" + str(twenty_four_hour_format)
                            else:
                                twenty_four_hour_format = "▲" + str(twenty_four_hour_format)
                                
                        if ticker_data.twenty_four_hour_change_pct <= 1 and ticker_data.twenty_four_hour_change_pct >=-1:
                            twenty_four_hour_pct_format = '{0:,.2f}'.format(abs(float(ticker_data.twenty_four_hour_change_pct)))
                            if float(ticker_data.twenty_four_hour_change_pct) < 0:
                                twenty_four_hour_pct_format = "▼" + str(twenty_four_hour_pct_format)
                            else:
                                twenty_four_hour_pct_format = "▲" + str(twenty_four_hour_pct_format)
                        else:
                            twenty_four_hour_pct_format = '{0:,.2f}'.format(abs(float(ticker_data.twenty_four_hour_change_pct)))
                            if float(ticker_data.twenty_four_hour_change_pct) < 0:
                                twenty_four_hour_pct_format = "▼" + str(twenty_four_hour_pct_format)
                            else:
                                twenty_four_hour_pct_format = "▲" + str(twenty_four_hour_pct_format)

                        if float(ticker_data.twenty_four_hour_change_pct) >= 0:
                            twenty_four_hour_color = Color.fg.green
                        else:
                            twenty_four_hour_color = Color.fg.red

                        if ticker_data.hour_change <= 1 and ticker_data.hour_change >=-1:
                            hour_format = '{0:,.8f}'.format(abs(float(ticker_data.hour_change)))
                            if float(ticker_data.hour_change_pct) < 0:
                                hour_format = "▼" + str(hour_format)
                            else:
                                hour_format = "▲" + str(hour_format)
                        else:
                            hour_format = '{0:,.2f}'.format(abs(float(ticker_data.hour_change)))
                            if float(ticker_data.hour_change_pct) < 0:
                                hour_format = "▼" + str(hour_format)
                            else:
                                hour_format = "▲" + str(hour_format)

                        if ticker_data.hour_change_pct <= 1 and ticker_data.hour_change_pct >=-1:
                            hour_pct_format = '{0:,.2f}'.format(abs(float(ticker_data.hour_change_pct)))
                            if float(ticker_data.hour_change_pct) < 0:
                                hour_pct_format = "▼" + str(hour_pct_format)
                            else:
                                hour_pct_format = "▲" + str(hour_pct_format)
                        else:
                            hour_pct_format = '{0:,.2f}'.format(abs(float(ticker_data.hour_change_pct)))
                            if float(ticker_data.hour_change_pct) < 0:
                                hour_pct_format = "▼" + str(hour_pct_format)
                            else:
                                hour_pct_format = "▲" + str(hour_pct_format)
                        
                        if float(ticker_data.hour_change_pct) >= 0:
                            hour_color = Color.fg.green
                        else:
                            hour_color = Color.fg.red

                    # Output for terminal        
                    coin_to_currency = str(coin + '-' + ticker_data.currency_symbol)
                    output += coin_to_currency.ljust(12,' ') \
                    + str(price_format).rjust(12,' ') + '\t' + twenty_four_hour_color \
                    + str(twenty_four_hour_format).rjust(12,' ') + '\t'\
                    + str('(' + twenty_four_hour_pct_format + '%)').rjust(10,' ') + hour_color \
                    + str(hour_format).rjust(12,' ') + '\t' \
                    + str('(' + hour_pct_format + '%)').rjust(10,' ') + Color.end \
                    + str(ticker_data.last_update + '\n').rjust(24,' ') \

                    # Output for led array
                    output_display += str(coin_to_currency + ": ").lower() \
                    + str(price_format) + str(' ' + hour_format + '    ')

        return output, output_display
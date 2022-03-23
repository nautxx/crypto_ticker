from datetime import datetime, timedelta
from color import Color
from ticker_data import TickerData

class TickerSearch:
    def __init__(self):
        pass

    def compare_crypto(self, data):
        output, output_display = "", ""

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
                            twenty_four_hour_format = '{0:+,.8f}'.format(float(ticker_data.twenty_four_hour_change))
                        else:
                            twenty_four_hour_format = '{0:+,.2f}'.format(float(ticker_data.twenty_four_hour_change))

                        if ticker_data.twenty_four_hour_change_pct <= 1 and ticker_data.twenty_four_hour_change_pct >=-1:
                            twenty_four_hour_pct_format = '{0:+,.2f}'.format(float(ticker_data.twenty_four_hour_change_pct))
                        else:
                            twenty_four_hour_pct_format = '{0:+,.2f}'.format(float(ticker_data.twenty_four_hour_change_pct))

                        if float(ticker_data.twenty_four_hour_change_pct) >= 0:
                            twenty_four_hour_color = Color.fg.green
                        else:
                            twenty_four_hour_color = Color.fg.red

                        if ticker_data.hour_change <= 1 and ticker_data.hour_change >=-1:
                            hour_format = '{0:+,.8f}'.format(float(ticker_data.hour_change))
                        else:
                            hour_format = '{0:+,.2f}'.format(float(ticker_data.hour_change))

                        if ticker_data.hour_change_pct <= 1 and ticker_data.hour_change_pct >=-1:
                            hour_pct_format = '{0:+,.2f}'.format(float(ticker_data.hour_change_pct))
                        else:
                            hour_pct_format = '{0:+,.2f}'.format(float(ticker_data.hour_change_pct))
                            
                        if float(ticker_data.hour_change_pct) >= 0:
                            hour_color = Color.fg.green
                        else:
                            hour_color = Color.fg.red
                            
                coin_to_currency = str(coin + '-' + ticker_data.currency_symbol)
                output += coin_to_currency.ljust(12,' ') \
                + str(price_format).rjust(12,' ') + '\t' + twenty_four_hour_color \
                + str(twenty_four_hour_format).rjust(12,' ') + '\t'\
                + str('(' + twenty_four_hour_pct_format + '%)').rjust(10,' ') + hour_color \
                + str(hour_format).rjust(12,' ') + '\t' \
                + str('(' + hour_pct_format + '%)').rjust(10,' ') + Color.end \
                + str(ticker_data.last_update + '\n').rjust(24,' ') \

                output_display += str(coin_to_currency + ": ").lower() \
                + str(price_format) + str(' ' + hour_format + '    ')

        return output, output_display
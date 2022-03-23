from datetime import datetime, timedelta
from color import Color

class TickerSearch:
    def __init__(self):
        pass

    def compare_crypto(self, data):
        output, output_display = "", ""

        for coin in data['RAW']:
            for currency in data['RAW'][coin]:
                if coin != currency:
                    for category in data['RAW'][coin][currency]:
                        currency_symbol = data['RAW'][coin][currency]['TOSYMBOL']
                        price = data['RAW'][coin][currency]['PRICE']
                        last_update = (datetime.fromtimestamp(data['RAW'][coin][currency]['LASTUPDATE']) - timedelta(hours=0)).strftime('%Y-%m-%d %H:%M:%S')
                        twenty_four_hour_low = data['RAW'][coin][currency]['LOW24HOUR']
                        twenty_four_hour_high = data['RAW'][coin][currency]['HIGH24HOUR']
                        twenty_four_hour = data['RAW'][coin][currency]['CHANGE24HOUR']
                        twenty_four_hour_pct = data['RAW'][coin][currency]['CHANGEPCT24HOUR']
                        hour = data['RAW'][coin][currency]['CHANGEHOUR']
                        hour_pct = data['RAW'][coin][currency]['CHANGEPCTHOUR']
                        supply = data['RAW'][coin][currency]['SUPPLY']

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
                            twenty_four_hour_color = Color.fg.green
                        else:
                            twenty_four_hour_color = Color.fg.red

                        if hour <= 1 and hour >=-1:
                            hour_format = '{0:+,.8f}'.format(float(hour))
                        else:
                            hour_format = '{0:+,.2f}'.format(float(hour))

                        if hour_pct <= 1 and hour_pct >=-1:
                            hour_pct_format = '{0:+,.2f}'.format(float(hour_pct))
                        else:
                            hour_pct_format = '{0:+,.2f}'.format(float(hour_pct))
                            
                        if float(hour_pct) >= 0:
                            hour_color = Color.fg.green
                        else:
                            hour_color = Color.fg.red

                output += str(coin + '-' + currency_symbol).ljust(12,' ') \
                + str(price_format).rjust(12,' ') + '\t' + twenty_four_hour_color \
                + str(twenty_four_hour_format).rjust(12,' ') + '\t'\
                + str('(' + twenty_four_hour_pct_format + '%)').rjust(10,' ') + hour_color \
                + str(hour_format).rjust(12,' ') + '\t' \
                + str('(' + hour_pct_format + '%)').rjust(10,' ') + Color.end \
                + str(last_update + '\n').rjust(24,' ') \

                output_display += str(str(coin + '-' + currency_symbol + ": ")).lower() \
                + str(price_format) + str(' ' + hour_format + '    ')

        return output, output_display
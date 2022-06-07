class TickerData:
    """
    Retains data obtained from get_crypto_data
    """
    def __init__(
        self, currency_symbol, price, last_update, twenty_four_hour_low, 
        twenty_four_hour_high, twenty_four_hour_change, 
        twenty_four_hour_change_pct, hour_change, hour_change_pct, supply
        ):
        
        self.currency_symbol = currency_symbol
        self.price = price
        self.last_update = last_update
        self.twenty_four_hour_low = twenty_four_hour_low
        self.twenty_four_hour_high = twenty_four_hour_high
        self.twenty_four_hour_change = twenty_four_hour_change
        self.twenty_four_hour_change_pct = twenty_four_hour_change_pct
        self.hour_change = hour_change
        self.hour_change_pct = hour_change_pct
        self.supply = supply
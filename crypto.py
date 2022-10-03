import argparse
import sys

from binance.client import Client
from pprint import pprint
import time
import math


def crypto_gain(value_crypt, percentage_crypt, figures_crypt) -> [tuple]:
    """
    :param value_crypt: value of the asset
    :type value_crypt: int
    :param percentage_crypt: percentage of the gains
    :type percentage_crypt: int
    :param figures_crypt: number of precision for the quantities
    :type figures_crypt: int
    :return:
    """
    active_value = value_crypt * (percentage_crypt / 100) + value_crypt
    stop_lost = value_crypt - (value_crypt * (percentage_crypt - 0.5) / 200)
    limit = value_crypt - value_crypt * (percentage_crypt / 200)
    return round(active_value, figures_crypt), round(stop_lost, figures_crypt), round(limit, figures_crypt)


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


if __name__ == '__main__':
    start = time.time()
    # Parser of the script
    parser = argparse.ArgumentParser(usage='Insert the value following the percentage of profit '
                                           'and the number of figures')
    parser.add_argument('-c', '--coin', type=str, help='Coin to use in the trade')
    parser.add_argument('-pc', '--pair_coin', type=str, help='Pair coin of the trade', default='BUSD')
    parser.add_argument('-p', '--percentage', type=float, help='percentage of the profit', default=1.5)

    args = parser.parse_args()
    coin = args.coin
    pair_coin = args.pair_coin
    sym = coin + pair_coin
    percentage = args.percentage

    # Binance key for the API
    api_key = 'cOg0foUAY3Hfs7e3qKda9aBaWbAueKkw9sMJmvVgt59KL9ctlZtPpkDU4hdzGs1e'
    secret_key = 'XeT2tY41Bc9JJchKFrxEpw4YSNWaMgdSMjFnlIhUaq8ZSkbWmzTuWSQxQSPN0YHq'

    # Connect with the Binance client
    client = Client(api_key, secret_key)

    # Get the free cash available in the spot wallet
    info = client.get_account()
    balance = info['balances']
    free_cash = None
    for dict_assets in balance:
        try:
            if coin in dict_assets.values():
                free_cash = dict_assets['free']
        except TypeError:
            print('The coin is not in the current balance')
    print(free_cash)

    for kline in client.get_historical_klines_generator(sym, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
        pprint(kline)

    # Get the precision for the values of the trade
    info_coins = client.get_symbol_info(sym)
    figures = info_coins['baseAssetPrecision']
    price_precision = info_coins['filters'][0]['minPrice']
    price_precision = price_precision.split('1')
    figures = len(price_precision[0]) - 1

    lot_size = info_coins['filters'][2]['minQty']
    lot_size = lot_size.split('1')
    # optional way to truncate amt_str = "{:0.0{}f}".format(amount, precision)
    coin_quantity = truncate(float(free_cash), len(lot_size[0]) - 1)

    # Get the quantity of the last trade
    trades = client.get_my_trades(symbol=sym)
    if trades[-1]['isBuyer']:
        value = float(trades[-1]['price'])
    else:
        print(f'The last trade of {coin} was not a buy order')
        sys.exit(-1)
    print(value)

    active_value_c, stop_lost_c, limit_c = crypto_gain(value, percentage, figures)
    print(crypto_gain(value, percentage, figures))

    # Place an OCO sell order for the coin
    order = client.order_oco_sell(
        symbol=sym,
        stopLimitTimeInForce='GTC',
        quantity=coin_quantity,
        stopPrice=str(stop_lost_c),
        stopLimitPrice=str(limit_c),
        price=str(active_value_c),
    )
    client.close_connection()
    end = time.time()
    print("The time of execution of above program is :", (end - start) * 10 ** 3, "ms")



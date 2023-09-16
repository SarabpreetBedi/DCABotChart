from service.binance_service import *
from system.store_order import *
from system.load_data import *
from service.email_service import *
from trades.metrics import *

from datetime import datetime, time
import time
from system.logger import logger
import os.path


# load coins to DCA
coins_to_DCA = load_data('config/coins.yml')['COINS']
CRYPTOS =  load_data('config/coins.yml')['COINS']
CURRENCY = 'USD'

# loads local configuration
config = load_data('config/config.yml')


def main():
    """
    DCA every x number of days.
    """
    while True:

        # load the order file if it exists
        if os.path.isfile('trades/order.json'):
            order = load_order('trades/order.json')
        else:
            logger.info("No order file found, creating new file")
            order = {}

        pairing = config['TRADE_OPTIONS']['PAIRING']
        qty = config['TRADE_OPTIONS']['QUANTITY']
        frequency = config['TRADE_OPTIONS']['DCA_EVERY']
        test_mode = config['TRADE_OPTIONS']['TEST']
        send_notification_flag = config['SEND_NOTIFICATIONS']

        if not test_mode:
            logger.warning("RUNNING IN LIVE MODE! PAUSING FOR 1 MINUTE")
            time.sleep(60)

        # DCA each coin
        for coin in coins_to_DCA:
            last_price = get_price(coin, pairing)
            volume = convert_volume(coin+pairing, qty, last_price)

            try:
                # Run a test trade if true
                if config['TRADE_OPTIONS']['TEST']:
                    if coin not in order:
                        order[coin] = {}
                        order[coin]["orders"] = []

                    order[coin]["orders"].append({
                                'symbol':coin+pairing,
                                'price':last_price,
                                'volume':volume,
                                'time':datetime.timestamp(datetime.now())
                                })

                    logger.info('PLACING TEST ORDER')

                # place a live order if False
                else:
                    if coin not in order:
                        order[coin] = {}
                        order[coin]["orders"] = []

                    order[coin]["orders"] = create_order(coin+pairing, volume)

            except Exception as e:
                logger.info(e)

            else:
                logger.info(f"Order created with {volume} on {coin} at {datetime.now()}")
                store_order('trades/order.json', order)

        message = f'DCA complete, bought {coins_to_DCA}. Waiting {frequency} days.'
        logger.info(message)

        # sends an e-mail if enabled.
        if send_notification_flag:
            send_notification(message)

        # report on DCA performance. Files saved in trades/dca-tracker
        all_prices = get_all_order_prices(order)
        avg_dca = calculate_avg_dca(all_prices)
        dca_history = plot_dca_history(all_prices, avg_dca)
        
        crypto_data = dict()
        
        for crypto in CRYPTOS:
            crypto_data[crypto] = getData(crypto)
            
        fig = go.Figure()

         # Candlestick
        for idx, name in enumerate(crypto_data):
            fig = fig.add_trace(
                go.Candlestick(
                    x = crypto_data[name].index,
                    open = crypto_data[name].Open,
                    high = crypto_data[name].High,
                    low = crypto_data[name].Low,
                    close = crypto_data[name].Close,
                    name = name,
                )
            )

        # Scatter
        for idx, name in enumerate(crypto_data):
            fig = fig.add_trace(
                go.Scatter(
                    x = crypto_data[name].index,
                    y = crypto_data[name].Close,
                    name = name,
                )
            )

        fig.update_layout(
            title = 'The Correlation between Different Cryptocurrencies',
            xaxis_title = 'Date',
            yaxis_title = f'Closing price ({CURRENCY})',
            legend_title = 'Cryptocurrencies'
        )
        fig.update_yaxes(type='log', tickprefix='$')

        fig.show()

        time.sleep(frequency*86400)

    

if __name__ == '__main__':
    logger.info('working...')
    main()
   
    
  
    


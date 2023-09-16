from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import yaml
from system.load_data import load_data

from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


def get_all_order_prices(order):
    """
    Takes a dict of all orders and organises the last_price
    """
    coin_stats = {}
    for coin in order:
        coin_stats[coin] = []
        for item in order[coin]['orders']:
            coin_stats[coin].append(float(item['price']))

    return coin_stats


def calculate_avg_dca(data):
    """
    Takes a dict of lists cotaining last prices for each coin DCad
    And calculates the average DCA price for each coin
    """
    avg_dca = {}
    for coin in data:
        avg_dca[coin] = np.array(data[coin])
        avg_dca[coin] = np.average(avg_dca[coin])

    return avg_dca


def plot_dca_history(data, average):
    for coin in data:
        plt.plot(data[coin])
        plt.title(f'{coin} | Average {round(average[coin], 3)}')
        plt.savefig(f'trades/dca-tracker/{coin}.png')
        #plt.clf()
        plt.show()

def getData(cryptocurrency):
    
    CURRENCY = 'USD'
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    last_year_date = (now - timedelta(days=365)).strftime("%Y-%m-%d")

    start = pd.to_datetime(last_year_date)
    end = pd.to_datetime(current_date)
    yf.pdr_override() # <== that's all it takes :-)
    data = pdr.get_data_yahoo(f'{cryptocurrency}-{CURRENCY}', start, end)

    return data




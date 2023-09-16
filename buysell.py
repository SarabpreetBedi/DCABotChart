
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from datetime import date

from datetime import datetime, time, timedelta
from datetime import datetime
import time 
from system.load_data import *


plt.style.use('fivethirtyeight')
yf.pdr_override()


CRYPTOS =  load_data('config/coins.yml')['COINS']
CURRENCY = 'USD'

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
last_year_date = (now - timedelta(days=365)).strftime("%Y-%m-%d")
startdate = pd.to_datetime(last_year_date[:10])
end_date = pd.to_datetime(current_date)

def getMyPortfolio(stocksymbols):
    
    data = web.get_data_yahoo(f'{stocksymbols}-{CURRENCY}', startdate  ,end_date)
    return data

def buy_sell(data):
    signalBuy = []
    signalSell = []
    position = False 

    for i in range(len(data)):
        if data['SMA 30'][i] > data['SMA 100'][i]:
            if position == False :
                signalBuy.append(data['Adj Close'][i])
                signalSell.append(np.nan)
                position = True
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        elif data['SMA 30'][i] < data['SMA 100'][i]:
            if position == True:
                signalBuy.append(np.nan)
                signalSell.append(data['Adj Close'][i])
                position = False
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        else:
            signalBuy.append(np.nan)
            signalSell.append(np.nan)
    return pd.Series([signalBuy, signalSell])

list = []
for crypto in CRYPTOS:
            list.append(crypto)
for a in list:
     print(a)
     data = getMyPortfolio(a)
     data['SMA 30'] = ta.sma(data['Close'],30)
     data['SMA 100'] = ta.sma(data['Close'],100)
     data['Buy_Signal_price'], data['Sell_Signal_price'] = buy_sell(data)
     fig, ax = plt.subplots(figsize=(14,8))
     ax.plot(data['Adj Close'] , label = a ,linewidth=0.5, color='blue', alpha = 0.9)
     ax.plot(data['SMA 30'], label = 'SMA30', alpha = 0.85)
     ax.plot(data['SMA 100'], label = 'SMA100' , alpha = 0.85)
     ax.scatter(data.index , data['Buy_Signal_price'] , label = 'Buy' , marker = '^', color = 'green',alpha =1 )
     ax.scatter(data.index , data['Sell_Signal_price'] , label = 'Sell' , marker = 'v', color = 'red',alpha =1 )
     ax.set_title(a + " Price History with buy and sell signals",fontsize=10, backgroundcolor='blue', color='white')
     ax.set_xlabel(f'{startdate} - {end_date}' ,fontsize=18)
     ax.set_ylabel('Close Price USD ($)' , fontsize=18)
     legend = ax.legend()
     ax.grid()
     plt.tight_layout()
     plt.savefig(f'trades/dca-tracker/{a}_buysell.png')
     plt.show()


time.sleep(86400)


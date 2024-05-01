from Login_Zerodha import login_in_zerodha
from kiteconnect import KiteConnect
from GenerateBasket2 import GenerateBasket
from Store.Strategies import Strategies
import json , os , time , requests,datetime , threading , sys
from Functions import Store  , Script , ExtraFunctions
from Store import Cred
import talib 
import numpy as np
import pandas as pd


ZerodhaApis = []

ZerodhaAccounts = []

global TradeFunctionStart



def addZerodhaAccount(Credentials):
    ZerodhaAccounts.append(Credentials)

addZerodhaAccount(Cred.Crosshair)


for ZerodhaAccount in ZerodhaAccounts :
    LoginArray = []
    try :
        ExtraFunctions.ZerodhaApiLogin(ZerodhaAccount)
    except Exception as e:
        LoginArray.append(ZerodhaAccount)
        
    Threads = []
    
    for ZerodhaAccount in LoginArray:
        T = threading.Thread(target=login_in_zerodha , args= [ZerodhaAccount])
        T.start()
        Threads.append(T)
    for Thread in Threads :
     Thread.join()

    ZerodhaApis.append(ExtraFunctions.ZerodhaApiLogin(ZerodhaAccount))





Day = datetime.datetime.now().isoweekday()
Day = 4
MainAPI = ExtraFunctions.ZerodhaApiLogin(Cred.Crosshair)
close = []
high = []
low = []

data = MainAPI['API'].historical_data( 9982978, "2023-11-06 9:15:00", "2023-11-07 15:30:00", "minute", continuous=False, oi=False)
print(data)

for i in data:
    close.append(float(i['close']))
    high.append(float(i['high']))
    low.append(float(i['low']))
    
# print(close , low , high)

# def ema(values, period):
#     values = nd.array(values)
#     return pd.ema(values, span=period)[-1]

# values = close
# period = 33
print(talib.EMA(np.array(close),timeperiod =33 ))

# atr = talib.ATR(np.array(high),np.array(low),np.array(close),14)
# print (atr)

# print (ema(values, period))


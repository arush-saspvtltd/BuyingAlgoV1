
from kiteconnect import KiteConnect
import os
import threading
import json
from datetime import datetime
from Store import Cred
import math
import time
from Store.Strategies import Strategies 
from Functions import FindExpiry , currentStrike

import requests
URL ="https://api.kite.trade/instruments"
response = requests.get(URL)
open("instruments.txt", "wb").write(response.content)
global JSONFILE 
JSONFILE = {}

def CapitalZerodha(api):
        capital = api.margins()
      
        capital = (capital.get("equity").get("available").get("cash") + (capital).get("equity").get("available").get("collateral")+(capital).get("equity").get("available").get("intraday_payin"))
        UID =api.profile()['user_id']
        if UID == 'HPG489':
            capital = 1000
            
        return capital , UID

def RunBasket(api , atmStrike ,  Strategy , expiryDate  , Multiplier  , StrategyNo , Broker, Cred):
    HedgeCode = Strategy["Index"] + "24"  + expiryDate + str(atmStrike - Strategy["HedgeStrike"]) + "PE"
    peCode = Strategy["Index"] + "24"  + expiryDate + str(atmStrike-Strategy['Strike']) + "PE"
    
    exchange = "NFO"
    if Strategy["Index"] == "NIFTY":
        QtySlicer =25
     
    elif Strategy["Index"] == "FINNIFTY":
        QtySlicer =40
    elif Strategy["Index"] == "BANKNIFTY":
        QtySlicer =15
     
    elif Strategy["Index"] == "MIDCPNIFTY":
        QtySlicer =75
      
    elif(Strategy["Index"] =="SENSEX"):  
      exchange = "BFO"
      QtySlicer =10

    
    Capital , UserID = CapitalZerodha(api)
    Capital = Capital *Multiplier
    Qty =0

    hedgeQty = 0
    newQty = 0
    newHedgeQty = 0
    
    capital =  Capital
    requiredCapital =0 
    while (newHedgeQty <=newQty*1):
     
        oldBasket =[
            {
                "exchange": exchange,
                "tradingsymbol": HedgeCode,
                "transaction_type": "BUY",
                "variety": "regular",
                "product": "NRML",
                "order_type": "MARKET",
                "quantity": hedgeQty,
                "price": 0,
                "trigger_price": 0
            },
            {
                "exchange": exchange,
                "tradingsymbol": peCode,
                "transaction_type": "SELL",
                "variety": "regular",
                "product": "NRML",
                "order_type": "MARKET",
                "quantity": Qty,
                "price": 0,
                "trigger_price": 0
            },
        ]
        newBasket = [
            {
                "exchange": exchange,
                "tradingsymbol": HedgeCode,
                "transaction_type": "BUY",
                "variety": "regular",
                "product": "NRML",
                "order_type": "MARKET",
                "quantity": newHedgeQty,
                "price": 0,
                "trigger_price": 0
            },
            {
                "exchange": exchange,
                "tradingsymbol": peCode,
                "transaction_type": "SELL",
                "variety": "regular",
                "product": "NRML",
                "order_type": "MARKET",
                "quantity": newQty,
                "price": 0,
                "trigger_price": 0
            },
        ]
        
        
        requiredCapital = api.basket_order_margins(newBasket, consider_positions=True, mode=None).get('initial').get('total')
        # print(requiredCapital)
        if(requiredCapital<capital):
            Qty = newQty
            hedgeQty = newHedgeQty
            
        # print(newHedgeQty, newQty, requiredCapital)
        if(requiredCapital< capital):
            
            newQty = newQty+QtySlicer
        
        if(requiredCapital> capital):
            
            newHedgeQty = newHedgeQty+QtySlicer

    JSONFILE[UserID + "_" + StrategyNo] = {
    "Name":UserID + "_" + StrategyNo ,
    "HedgeQty": hedgeQty,
    "Qty": Qty,
    "Cred":Cred,
    "Broker":Broker,
    "Strategy":StrategyNo
    }
    print("Best Case Scenario " + "Hedge Qty: " + str(hedgeQty) +" , Qty: " + str(Qty) + " , Margin Required: "+str( api.basket_order_margins(oldBasket, consider_positions=True, mode=None).get('initial').get('total')) +" Capital " +str(Capital)+" "+UserID + "_" + StrategyNo )

    
    
def GenerateBasket(ZerodhaAPIs):
    Day = datetime.now().isoweekday()
    SeparateArray = [""]
    Strategy  = Strategies[str(Day)]
    Broker = "Zerodha"
    Index = Strategy["1"]['Index']
    atmStrike = currentStrike.currentStrike(ZerodhaAPIs[0]['API'] , Index , 0 , 0 , 0 , 0)
    expiryDate = FindExpiry.findExpiry(Index , atmStrike)
    Threads =[]
    for API in  ZerodhaAPIs:
        Split =0.2
        if Day == 1:
            Split =  0.1
        if Day == 2:
            Split =  0.2
        if Day == 3:
            Split =  0.18
        if Day == 4:
            Split =  0.23
        if Day == 5:
            Split =  0.1
        # if day == "3":
        #     split =  0.2
            
        
        t1= threading.Thread(target = RunBasket , args=[API["API"] ,atmStrike , Strategy["1"] ,expiryDate ,Split , "1" , Broker, API["Cred"] ])
        t2= threading.Thread(target = RunBasket , args=[API["API"] ,atmStrike , Strategy["2"] ,expiryDate ,Split , "2" , Broker, API["Cred"] ])
        t3= threading.Thread(target = RunBasket , args=[API["API"] ,atmStrike , Strategy["3"] ,expiryDate ,Split , "3" , Broker, API["Cred"] ])
        t4= threading.Thread(target = RunBasket , args=[API["API"] ,atmStrike , Strategy["4"] ,expiryDate ,Split , "4" , Broker, API["Cred"] ])
                    
        Threads.append(t1)
        Threads.append(t2)
        Threads.append(t3)
        Threads.append(t4)


            
    for thread in Threads:
             
            thread.start()
    for thread in Threads:
            
            thread.join()
    out_file = open("Quantity.json", "w")

    json.dump(JSONFILE, out_file, indent = 6)

    return (JSONFILE)    

    
    
    
    
    


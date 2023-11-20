import time
try:
    import Cred
    from kiteconnect import KiteConnect
    import json
    import currentStrike , FindExpiry , datetime , talib , requests  , datetime
    import numpy as np
    import pandas as pd

    Credentials = Cred.Crosshair

    
    URL ="https://api.kite.trade/instruments"
    response = requests.get(URL)
    open("instruments.txt", "wb").write(response.content)

    file = open("/Users/crosshair/Documents/GitHub/BuyingAlgoV1/AccessToken/"+Credentials["user_id"] + '.txt', 'r')

    Credentials['access_token'] = file.read()
    api = KiteConnect(api_key=Credentials["api_key"])
    api.set_access_token(Credentials["access_token"])


    
    with open('Variables.json', 'r') as openfile:
    
        # Reading from json file
        Variables = json.load(openfile)

    # print(Variables)

    OptionType = "CE"

    ATM = currentStrike.currentStrike(api , Variables['Index'] , 0 , 0, 0, 0 )
    print(ATM)

    ltpType = "NFO:"
    StrikeDifference = 0

    exchange = "NFO"
    if Variables["Index"] == "NIFTY":
        QtySlicer =50
        StrikeDifference = 50
        MaxQuantity = 1800
        
    elif Variables["Index"] == "FINNIFTY":
            QtySlicer =40
            StrikeDifference = 50
            MaxQuantity = 1800

    elif Variables["Index"] == "BANKNIFTY":
            QtySlicer =15
            StrikeDifference = 100
            MaxQuantity = 900
        
    elif Variables["Index"] == "MIDCPNIFTY":
            QtySlicer =75
            StrikeDifference = 25
            MaxQuantity = 4200
        
    elif(Variables["Index"] =="SENSEX"):  
        exchange = "BFO"
        QtySlicer =10
        StrikeDifference = 100
        MaxQuantity = 1000
        ltpType = "BFO:"


    expiry = FindExpiry.findExpiry(Variables["Index"] , ATM)
    year = datetime.datetime.now().year % 100
    Symbol = ""
    price = 0
    
    while True:
        Symbol = Variables['Index'] + str( year) + expiry +str( ATM )+ OptionType
        # print(Symbol)
        price = api.ltp(ltpType+Symbol).get(ltpType+Symbol)
        instrument_token = price.get('instrument_token')
        price = price.get('last_price')
        if price > Variables['BuyPrice']:
            break
        else :
            ATM = ATM - StrikeDifference 
    
    print(price , Symbol)
    
    StopLoss =0
    StopLoss = input("Please Enter StopLoss:- ")
        
    StopLoss = int(StopLoss)
    

    # Calculate yesterday's date
    

    lots  = int((Variables["MaxLoss"] / StopLoss )/QtySlicer)
    qty =  (lots) * QtySlicer
    print(qty)
    
    
    StopLossOrders =[]
    Type = Variables['ProductType']
    while (qty >MaxQuantity):

                    api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_BUY,
                                            quantity=MaxQuantity,
                                            order_type=api.ORDER_TYPE_MARKET,
                                            
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                    qty = qty- MaxQuantity
                
    if qty > 0:
                            
                        api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_BUY,
                                            quantity=qty,
                                            order_type=api.ORDER_TYPE_MARKET,
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                        print("Order Placed")
    lots  = int((Variables["MaxLoss"] / StopLoss )/QtySlicer)
    qty =  (lots) * QtySlicer
    print(qty)
    while (qty > MaxQuantity):

                    order=  api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=MaxQuantity,
                                            order_type=api.ORDER_TYPE_SL,
                                            trigger_price=price -StopLoss,
                                            price= price -StopLoss + Variables['TriggerDifference'], 
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                    qty = qty- MaxQuantity
                    StopLossOrders.append(order)
                
    if qty > 0:
                            
                        order=    api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=qty,
                                            order_type=api.ORDER_TYPE_SL,
                                            trigger_price=price -StopLoss,
                                            price= price -StopLoss + Variables['TriggerDifference'],
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                        print("Order Placed")
    lots  = int((Variables["MaxLoss"] / StopLoss )/QtySlicer)
    qty =  (lots) * QtySlicer
    
    print(qty)   
    while True:
        time.sleep(0.3)
        if api.ltp(ltpType+Symbol).get(ltpType+Symbol).get('last_price') > price *Variables['FirstTargetMultiplier']:
            SquareOffQuantity = int(int(qty/QtySlicer)/2) *QtySlicer
            
            while (SquareOffQuantity >MaxQuantity):

                    api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=MaxQuantity,
                                            order_type=api.ORDER_TYPE_MARKET,
                                            
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                    SquareOffQuantity = SquareOffQuantity- MaxQuantity
                
            if SquareOffQuantity > 0:
                            
                        api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=SquareOffQuantity,
                                            order_type=api.ORDER_TYPE_MARKET,
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                        print("Order Placed")
            break
        
    orderbook = api.orders()
   

    for order in orderbook:
        
        if order['status']=="TRIGGER PENDING":
                print(order)
                api.cancel_order("regular",order["order_id"])
    lots  = int((Variables["MaxLoss"] / StopLoss )/QtySlicer)
    qty =  (lots - int(lots/2) )* QtySlicer
    
    while (qty > MaxQuantity):

                    order=  api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=MaxQuantity,
                                            order_type=api.ORDER_TYPE_SL,
                                            trigger_price=price,
                                            price= price  + Variables['TriggerDifference'], 
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                    qty = qty- MaxQuantity
                    StopLossOrders.append(order)
                
    if qty > 0:
                            
                        order=    api.place_order(variety=api.VARIETY_REGULAR,
                                            tradingsymbol=Symbol,
                                            exchange=exchange,
                                            transaction_type=api.TRANSACTION_TYPE_SELL,
                                            quantity=qty,
                                            order_type=api.ORDER_TYPE_SL,
                                            trigger_price=price ,
                                            price= price  + Variables['TriggerDifference'],
                                            product=Type,
                                            validity=api.VALIDITY_DAY)
                        print("Order Placed")
    
    print(qty)   
    while True:
        time.sleep(0.3)

        if api.ltp(ltpType+Symbol).get(ltpType+Symbol).get('last_price') > price *Variables['ExitTargetMultiplier']:
            orderbook = API.orders()
   

            for order in orderbook:
            
                if order['status']=="TRIGGER PENDING":
                    print(order)
                    API.cancel_order("regular",order["order_id"])
                    print(order)


            positions = API.positions()

        # for position in positions['day']:
        #     # if position['quantity'] ==0 :
        #         print(position['quantity'])
            for position in positions['net']:
                
                if position['quantity'] !=0 :
                    print(position)
                    if position['quantity']<0 :
                        qty = abs(position['quantity'])
                        while(qty > qtySlicer):
                            API.place_order(variety=API.VARIETY_REGULAR,
                                                        tradingsymbol=position['tradingsymbol'],
                                                        exchange=exchange,
                                                        transaction_type=API.TRANSACTION_TYPE_BUY,
                                                        quantity=qtySlicer,
                                                        order_type=API.ORDER_TYPE_MARKET,
                                                        product=position["product"],
                                                        validity=API.VALIDITY_DAY)
                            qty = qty -qtySlicer
                            
                        API.place_order(variety=API.VARIETY_REGULAR,
                                                        tradingsymbol=position['tradingsymbol'],
                                                        exchange=exchange,
                                                        transaction_type=API.TRANSACTION_TYPE_BUY,
                                                        quantity=qty,
                                                        order_type=API.ORDER_TYPE_MARKET,
                                                        product=position["product"],
                                                        validity=API.VALIDITY_DAY)
                    if position['quantity']>0 :
                        qty = abs(position['quantity'])
                        while(qty > qtySlicer):
                            API.place_order(variety=API.VARIETY_REGULAR,
                                                        tradingsymbol=position['tradingsymbol'],
                                                        exchange=exchange,
                                                        transaction_type=API.TRANSACTION_TYPE_SELL,
                                                        quantity=qtySlicer,
                                                        order_type=API.ORDER_TYPE_MARKET,
                                                        product=position["product"],
                                                        validity=API.VALIDITY_DAY)
                            qty = qty -qtySlicer
                            
                        API.place_order(variety=API.VARIETY_REGULAR,
                                                        tradingsymbol=position['tradingsymbol'],
                                                        exchange=exchange,
                                                        transaction_type=API.TRANSACTION_TYPE_SELL,
                                                        quantity=qty,
                                                        order_type=API.ORDER_TYPE_MARKET,
                                                        product=position["product"],
                                                        validity=API.VALIDITY_DAY)
        break


except Exception as e:
      raise Exception(e)
      time.sleep(10000)



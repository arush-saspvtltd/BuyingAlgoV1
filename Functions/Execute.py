
from Functions import Execute
from kiteconnect import KiteTicker
from time import sleep
from Functions import Store
import requests , math  , threading , datetime , os ,sys , time ,json
def send_to_telegram(message):
    
    try:
        apiToken = '6058041177:AAHhrqXPDRa1vghxQu_dTyTXTar1JRgNjCo'
        chatID = '1083941928'
        apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

def sl(ApiZerodha ,Variables,QuantityJSON , Cred , TradeFunctionStart , StrategyNo):
    
    
    
    kws = KiteTicker(Cred['api_key'], Cred["access_token"])

    def on_ticks(ws, ticks):  # noqa
        # Callback to receive ticks.
        
        now = datetime.datetime.now()

        if(len(ticks)==2):
         
            # os.system('clear')
            # print(Variables["Name"])
            # print(now.hour, ":", now.minute, ":", now.second)
            # print(Store.status[StrategyNo])
            # print(Store.AtmStrike[StrategyNo])
            # print(Variables["Index"])
            # print("StopLoss:", Store.stopLoss[StrategyNo])
            # print("Price:", Store.Price[StrategyNo])
            c =0
            p =0
            if ("instrument_token" in ticks[0] and Store.ZerodhaToken[StrategyNo]["CE"] == ticks[0]['instrument_token']):
            
             
             Store.Global_Status[('Strategy'+ StrategyNo+ "Price")] ={
                        'CE' : ticks[0]['last_price'] ,
                        'PE' : ticks[1]['last_price'] ,
                       
                    }
             c=0
             p=1
            else:
                # print("CE Price:", ticks[1]['last_price'])  
                # print("PE Price:", ticks[0]['last_price'])
                Store.Global_Status[('Strategy'+ StrategyNo+ "Price")] ={
                        'CE' : ticks[1]['last_price'] ,
                        'PE' : ticks[0]['last_price'] ,
                   
                    } 

                c=1
                p=0
            
            # Store.Global_Status[('Strategy'+ StrategyNo+ "Price")]. )

           

            if (Store.status1[StrategyNo] == Store.Trading_Strategy_Started and "last_price" in ticks[c] and ticks[c]['instrument_token'] == Store.ZerodhaToken[StrategyNo]['CE'] and float(ticks[c]['last_price']) >= Store.stopLoss[StrategyNo]['CE']):
                
                # print(ticks[c]['last_price'])
                # Store.Global_Status[('Strategy'+ StrategyNo)].append(Store.stopLoss[StrategyNo] ,ticks[c]['last_price'] )

                Store.Global_Status[('Strategy'+ StrategyNo)].append(Store.CE_SL_HIT)
                Store.stopLoss[StrategyNo] = Store.Price[StrategyNo]

                # print(Store.CE_SL_HIT)
                if (Store.status[StrategyNo] == Store.PE_SL_HIT):
                    Store.status1[StrategyNo] = False
                    
                else:
                    Exchange = "NFO:"
                    HedgeBuy = 2
                    if  Variables["Index"] == "SENSEX":
                        Exchange = "BFO:"
                        HedgeBuy = 5
                    if  Variables["Index"] == "BANKNIFTY":
                        HedgeBuy = 3
                    
                    HedgeBuy = ApiZerodha.ltp(Exchange+Store.ZerodhaStrike[StrategyNo]['hedgePE'])[Exchange+Store.ZerodhaStrike[StrategyNo]['hedgePE']]['last_price']+HedgeBuy

                    Store.status1[StrategyNo] = Store.CE_SL_HIT
                    Store.status[StrategyNo] = Store.CE_SL_HIT

                    for Client in QuantityJSON:
                      Var = QuantityJSON[Client]
                      if(QuantityJSON[Client]["Broker"] =="Zerodha" and Variables["StrategyName"]  == QuantityJSON[Client]["Strategy"]):
                        t=  threading.Thread(target=ZerodhaPlaceOrder ,args =[QuantityJSON[Client]["API"], Var, Variables["Index"] , HedgeBuy , "PE",QuantityJSON[Client]['Name'] , StrategyNo] )
                        t.start()

                    
                    Store.status1[StrategyNo] = Store.CE_SL_HIT
                    Store.status[StrategyNo] = Store.CE_SL_HIT
                    send_to_telegram("Trade Done")
                    with open("Logs/" + StrategyNo + ".txt", "a") as file:
                         file.write(str(datetime.date.today()) + "\n")



            if (Store.status1[StrategyNo] == Store.Trading_Strategy_Started and "last_price" in ticks[p] and ticks[p]['instrument_token'] == Store.ZerodhaToken[StrategyNo]['PE'] and float(ticks[p]['last_price']) >= Store.stopLoss[StrategyNo]['PE']):
                # print("PE: ", ticks[0]['last_price'])
                Store.Global_Status[('Strategy'+ StrategyNo)].append(Store.PE_SL_HIT)
                Store.stopLoss[StrategyNo] = Store.Price[StrategyNo]

                # print("PE: ", ticks[0]['last_price'])
              
                if (Store.status[StrategyNo] == Store.CE_SL_HIT):
                    Store.status1[StrategyNo] = False

                else:
                    Store.status1[StrategyNo] = Store.PE_SL_HIT
                    Store.status[StrategyNo] = Store.PE_SL_HIT
                    Exchange = "NFO:"
                    HedgeBuy = 2
                    if  Variables["Index"] == "SENSEX":
                        Exchange = "BFO:"
                        HedgeBuy = 5
                    if  Variables["Index"] == "BANKNIFTY":
                        HedgeBuy = 3
                    
                    HedgeBuy = ApiZerodha.ltp(Exchange+Store.ZerodhaStrike[StrategyNo]['hedgeCE'])[Exchange+Store.ZerodhaStrike[StrategyNo]['hedgeCE']]['last_price']+HedgeBuy
                    for Client in QuantityJSON:
                      Var = QuantityJSON[Client]
                 
                      if(QuantityJSON[Client]["Broker"] =="Zerodha" and Variables["StrategyName"]  == QuantityJSON[Client]["Strategy"]):
                        t=  threading.Thread(target=ZerodhaPlaceOrder ,args =[QuantityJSON[Client]["API"], Var, Variables["Index"] , HedgeBuy , "CE", QuantityJSON[Client]['Name'], StrategyNo] )
                        t.start()

                
                    Store.status1[StrategyNo] = Store.PE_SL_HIT
                    Store.status[StrategyNo] = Store.PE_SL_HIT
                    send_to_telegram("Trade Done")
                    with open("Logs/" + StrategyNo + ".txt", "a") as file:
                         file.write(str(datetime.date.today()) + "\n")
                    


    def on_connect(ws, response):  # noqa
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        # print(Store.ZerodhaToken[StrategyNo]['CE'])
        ws.subscribe([Store.ZerodhaToken[StrategyNo]["CE"], Store.ZerodhaToken[StrategyNo]["PE"]])
        
        print("Connected")

        # Set RELIANCE to tick in `full` mode.
        # ws.set_mode(ws.MODE_FULL, [738561])


    def on_order_update(ws, data):
        
        # call option sold , status , qty , order type 
        print("Order Done")
        # logging.debug("Order update : {}".format(data))


    # Assign the callbacks.
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_order_update = on_order_update


    global socket_opened
    socket_opened = True
    global xd
    xd = ApiZerodha
    global minQty
    global maxQty
    if (Variables["Index"] == "BANKNIFTY"):
        minQty = 25
        maxQty = 900

    if (Variables["Index"] == "FINNIFTY"):
        minQty = 40
        maxQty = 1800

    if (Variables["Index"] == "NIFTY"):
        minQty = 50
        maxQty = 1800
    if (Variables["Index"] == "MIDCPNIFTY"):
        minQty = 75
        maxQty = 4200
    if (Variables["Index"] == "SENSEX"):
        minQty = 10
        maxQty = 1000

    # print(Store.ZerodhaToken[StrategyNo])

  


    
    # Infinite loop on the main thread. Nothing after this will run.
    # You have to use the pre-defined callbacks to manage subscriptions.
    kws.connect(threaded=True)
    
    while True:
        time.sleep(1)
def ZerodhaPlaceOrder(API,Var, Index , HedgeBuy  , OptionType , Name , StrategyNo):
    try:
        print("Zerodha Place Order")
        SlQty = Var["Qty"]
        
        Type = "NRML"
        if Index =="SENSEX":
                    exchange = API.EXCHANGE_BFO
                    Sell_Price = 0
                
        else: 
                    exchange = API.EXCHANGE_NFO
                    Sell_Price = 0
            
        
        if OptionType == "CE":
            HedgeTradingSymbol = Store.ZerodhaStrike[StrategyNo]['hedgeCE']
            TradingSymbol = Store.ZerodhaStrike[StrategyNo]['CE']
        elif  OptionType == "PE":
            HedgeTradingSymbol = Store.ZerodhaStrike[StrategyNo]['hedgePE']
            TradingSymbol = Store.ZerodhaStrike[StrategyNo]['PE']
        
        orderIDs = {
            'HedgeIDs':[],
            'IDs':[],
            'StopLossIDs' :[]
        }
        while (Var["HedgeQty"] > maxQty):

                            orderID = API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=HedgeTradingSymbol,
                                            exchange=exchange,
                                            transaction_type=API.TRANSACTION_TYPE_BUY,
                                            quantity=maxQty,
                                            order_type=API.ORDER_TYPE_LIMIT,
                                            product=Type,
                                            price = HedgeBuy,
                                            validity=API.VALIDITY_DAY)
                            # history = API.order_history(orderID)
                            # if history[-1]['status'] == "REJECTED":
                            #     orderID = API.place_order(variety=API.VARIETY_REGULAR,
                            #                 tradingsymbol=HedgeTradingSymbol,
                            #                 exchange=exchange,
                            #                 transaction_type=API.TRANSACTION_TYPE_BUY,
                            #                 quantity=maxQty,
                            #                 order_type=API.ORDER_TYPE_LIMIT,
                            #                 product=Type,
                            #                 price = HedgeBuy,
                            #                 validity=API.VALIDITY_DAY)
                                
                                

                            Var["HedgeQty"] = Var["HedgeQty"] - maxQty
                            
                            # orderIDs['HedgeIDs'].append(orderID)
                            

        if (Var["HedgeQty"] > 0):
                            
                            orderID = API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=HedgeTradingSymbol,
                                            exchange=exchange,
                                        transaction_type=API.TRANSACTION_TYPE_BUY,
                                            quantity=Var["HedgeQty"],
                                            order_type=API.ORDER_TYPE_LIMIT,
                                            price = HedgeBuy,
                                            product=Type,
                                            validity=API.VALIDITY_DAY)
                            print("Hedge")
                            # orderIDs['HedgeIDs'].append(orderID)
                            
                            # history = API.order_history(orderID)
                            # if history[-1]['status'] == "REJECTED":
                            #     orderID = API.place_order(variety=API.VARIETY_REGULAR,
                            #                 tradingsymbol=HedgeTradingSymbol,
                            #                 exchange=exchange,
                            #                 transaction_type=API.TRANSACTION_TYPE_BUY,
                            #                 quantity=Var["HedgeQty"],
                            #                 order_type=API.ORDER_TYPE_LIMIT,
                            #                 price = HedgeBuy,
                            #                 product=Type,
                            #                 validity=API.VALIDITY_DAY)
                            # orderIDs['HedgeIDs'].append(orderID)
                                

                            
        sleep(1)
        while (SlQty > maxQty):
                        
                            orderID = API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=TradingSymbol,
                                            exchange=exchange,
                                            transaction_type=API.TRANSACTION_TYPE_SELL,
                                            quantity=maxQty,
                                            order_type=API.ORDER_TYPE_MARKET,
                                            product=Type,
                                            validity=API.VALIDITY_DAY)
                            
                            
                            # orderIDs['IDs'].append(orderID)
                            SlQty = SlQty - maxQty
                                


        if (SlQty > 0):

                        orderID = API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=TradingSymbol,
                                            exchange=exchange,
                                            transaction_type=API.TRANSACTION_TYPE_SELL,
                                            quantity=SlQty,
                                            order_type=API.ORDER_TYPE_MARKET,
                                            product=Type,
                                            validity=API.VALIDITY_DAY)
                        # orderIDs['IDs'].append(orderID)

        time.sleep(1)                    
        
        SlQty = Var["Qty"]
        

        while (SlQty >= maxQty):
                        
                            orderID = API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=TradingSymbol,
                                            exchange=exchange,
                                        transaction_type=API.TRANSACTION_TYPE_BUY,
                                            quantity=maxQty,
                                            order_type=API.ORDER_TYPE_SL,
                                            price=math.ceil(Store.Price[StrategyNo][OptionType])+6,
                                            trigger_price=math.ceil(Store.Price[StrategyNo][OptionType]),
                                            product=Type,
                                            validity=API.VALIDITY_DAY)
                            SlQty = SlQty - maxQty
                            # history = API.order_history(orderID)
                            # if history[-1]['status'] == "REJECTED":
                            #      orderID = API.place_order(variety=API.VARIETY_REGULAR,
                            #                 tradingsymbol=TradingSymbol,
                            #                 exchange=exchange,
                            #                 transaction_type=API.TRANSACTION_TYPE_BUY,
                            #                 quantity=maxQty,
                            #                 order_type=API.ORDER_TYPE_SL,
                            #                 price=math.ceil(Store.stopLoss[StrategyNo]['CE'])+6,
                            #                 trigger_price=math.ceil(Store.stopLoss[StrategyNo]['CE']),
                            #                 product=Type,
                            #                 validity=API.VALIDITY_DAY)
                                
                            # orderIDs['StopLossIDs'].append(orderID)


        if(SlQty>0):
                        orderID = API.place_order(variety=API.VARIETY_REGULAR,
                                    tradingsymbol=TradingSymbol,
                                    exchange=exchange,
                                    transaction_type=API.TRANSACTION_TYPE_BUY,
                                    quantity=SlQty,
                                    order_type=API.ORDER_TYPE_SL,
                                    price=math.ceil(Store.Price[StrategyNo][OptionType]) + 6,
                                    trigger_price=math.ceil(Store.Price[StrategyNo][OptionType]),
                                    product=Type,
                                    validity=API.VALIDITY_DAY)
                        history = API.order_history(orderID)
                        # if history[-1]['status'] == "REJECTED":
                        #     orderID = API.place_order(variety=API.VARIETY_REGULAR,
                        #             tradingsymbol=TradingSymbol,
                        #             exchange=exchange,
                        #             transaction_type=API.TRANSACTION_TYPE_BUY,
                        #             quantity=SlQty,
                        #             order_type=API.ORDER_TYPE_SL,
                        #             price=math.ceil(Store.stopLoss[StrategyNo]['CE']) + 6,
                        #             trigger_price=math.ceil(Store.stopLoss[StrategyNo]['CE']),
                        #             product=Type,
                        #             validity=API.VALIDITY_DAY)
                                
                        # orderIDs['StopLossIDs'].append(orderID)
                            # SlQty = SlQty - minQty
        # time.sleep(5)
        # for order in orderIDs['IDs']:
        #     history = API.order_history(order)
        #     if history[-1]['status'] == "REJECTED":
        #                 orderID = API.place_order(variety=API.VARIETY_REGULAR,
        #                                     tradingsymbol=history[-1]['tradingsymbol'],
        #                                     exchange=history[-1]['exchange'],
        #                                     transaction_type=history[-1]['transaction_type'],
        #                                     quantity=history[-1]['quantity'],
        #                                     order_type=history[-1]['order_type'],
        #                                     product=history[-1]['product'],
        #                                     validity=API.VALIDITY_DAY)
                        # orderIDs['IDs'].append(orderID)
            
        # time.sleep(2)
        # for order in orderIDs['StopLossIDs']:
        #     history = API.order_history(order)
        #     if history[-1]['status'] == "REJECTED":
        #                 orderID = API.place_order(variety=API.VARIETY_REGULAR,
        #                                     tradingsymbol=history[-1]['tradingsymbol'],
        #                                     exchange=history[-1]['exchange'],
        #                                     transaction_type=history[-1]['transaction_type'],
        #                                     quantity=history[-1]['quantity'],
        #                                     order_type=history[-1]['order_type'],
        #                                     product=history[-1]['product'],
        #                                     price=history[-1]['price'],trigger_price=history[-1]['trigger_price'],
                                            
        #                                     validity=API.VALIDITY_DAY)
        
        # Store.Global_Status[('Strategy'+ StrategyNo)].append(orderIDs )
        # Store.Global_Status[('Strategy'+ StrategyNo)].append(Name )
        # out_file = open("Logs/RunningPositions/" + Name +".json", "a")

        # json.dump(orderIDs, out_file, indent = 6)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print("Error!!!")
        Store.Global_Status[('Strategy'+ StrategyNo)].append('Error in code , there for ended ' +" " + str(exc_type) +" " + str (fname)+" " +str (exc_tb.tb_lineno) +" " + str(e) )


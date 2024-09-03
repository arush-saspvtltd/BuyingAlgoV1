from Functions import currentStrike , Store
from os import system

import math , time , datetime,sys , os 
from Functions import Store , Execute , FindExpiry


def Search(ApiZerodha ,   Variables , QuantityJSON , Cred , TradeFunctionStart , StrategyNo , TradeAPI):

   
    exchange = "NFO:"
    if Variables["Index"] == "SENSEX":
            exchange ="BFO:"
    try:
            Store.ZerodhaToken[StrategyNo] = {}
            Store.Price[StrategyNo] = {}
            Store.stopLoss[StrategyNo] = {}
            Store.ZerodhaStrike[StrategyNo] = {}
            year = datetime.datetime.now().year %100
            current_time = datetime.datetime.now()
            # two_days = datetime.timedelta(days=1)
            endDate = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            # current_time = current_time -two_days
            formatted_time = current_time.strftime('%Y-%m-%d') +" 9:15:00"
            # time_block = int((int(Variables['Time'][0:2]) - (9))*12 + (int(Variables['Time'][3:5])- 15))
            time_block = int((datetime.datetime.strptime(Variables['Time'], "%H:%M:%S") - datetime.datetime.strptime( "09:15:00", "%H:%M:%S")).total_seconds()/60)
            Index = Variables['Index']

            Store.AtmStrike[StrategyNo] = currentStrike.currentStrike(
                ApiZerodha, Variables["Index"] , 1 ,formatted_time , endDate, time_block) 
            if Store.AtmStrike[StrategyNo] == None:
                Store.AtmStrike[StrategyNo] = currentStrike.currentStrike(
                ApiZerodha, Variables["Index"] , 1 ,formatted_time , endDate, time_block)
                
                
            Store.Global_Status[('Strategy'+ StrategyNo)].append(('Atm Strike Selected as '+str(Store.AtmStrike[StrategyNo])))

            
            atmStrike = currentStrike.currentStrike(ApiZerodha, Index , 0 , 0 , 0 , 0)
            expiryDate = FindExpiry.findExpiry(Index , atmStrike)
            if atmStrike == None:
                atmStrike = currentStrike.currentStrike(ApiZerodha, Index , 0 , 0 , 0 , 0)

                


            hedgeCE = ( Variables["Index"] + str(year) + expiryDate+
                                    str(Store.AtmStrike[StrategyNo] + Variables["HedgeStrike"]) + "CE")
            
            Store.ZerodhaStrike[StrategyNo]['hedgeCE'] = hedgeCE
            Store.ZerodhaToken[StrategyNo]['hedgeCE'] = hedgeCE

            hedgePE = ( Variables["Index"] + str(year) + expiryDate +
                                    str(Store.AtmStrike[StrategyNo] - Variables["HedgeStrike"]) + "PE")
            Store.ZerodhaStrike[StrategyNo]['hedgePE'] = hedgePE
            Store.ZerodhaToken[StrategyNo]['hedgePE'] = hedgePE

            CE = (Variables["Index"] + str(year) + expiryDate +
                                str(Store.AtmStrike[StrategyNo] + Variables["Strike"] ) + "CE")
            Store.ZerodhaStrike[StrategyNo]['CE'] = CE
            Store.ZerodhaToken[StrategyNo]['CE'] = CE

            PE = ( Variables["Index"] + str(year) + expiryDate +
                                str(Store.AtmStrike[StrategyNo]- Variables["Strike"] ) + "PE")
            Store.ZerodhaStrike[StrategyNo]['PE'] = PE
            Store.ZerodhaToken[StrategyNo]['PE'] = PE

            # Storing Price and StopLoss
            res = (ApiZerodha.ltp(exchange + CE)).get(exchange + CE)
            Store.Price[StrategyNo]['CE'] = (ApiZerodha.historical_data(res.get('instrument_token'), formatted_time, endDate, 'minute', continuous=False, oi=False))[time_block]['open']
            if Store.Price[StrategyNo]['CE'] == None :
                time.sleep(1)
                Store.Price[StrategyNo]['CE'] = (ApiZerodha.historical_data(res.get('instrument_token'), formatted_time, endDate, 'minute', continuous=False, oi=False))[time_block]['open']
            Store.ZerodhaToken[StrategyNo]['CE'] = res.get('instrument_token')

            Store.stopLoss[StrategyNo]['CE'] = (
                float(Store.Price[StrategyNo]['CE']) * (1 + Variables["StopLoss"] / 100))
            
            
            res = (ApiZerodha.ltp(exchange + PE)).get(exchange+PE)
            
            Store.Price[StrategyNo]['PE'] = (ApiZerodha.historical_data(res.get('instrument_token'), formatted_time, endDate, 'minute', continuous=False, oi=False))[time_block]['open']
            if Store.Price[StrategyNo]['PE'] == None :
                time.sleep(1)
                Store.Price[StrategyNo]['PE'] = (ApiZerodha.historical_data(res.get('instrument_token'), formatted_time, endDate, 'minute', continuous=False, oi=False))[time_block]['open']

            
            Store.ZerodhaToken[StrategyNo]['PE'] = res.get('instrument_token')
            
            Store.stopLoss[StrategyNo]['PE'] = (
                float(Store.Price[StrategyNo]['PE']) * (1 + Variables["StopLoss"] / 100))
            
            Store.Global_Status[('Strategy'+ StrategyNo)].append(("Price is CE: "+ str(round(Store.Price[StrategyNo]['CE'], 2)) + ' PE: '  +  str(round(Store.Price[StrategyNo]['PE'] , 2))))
            Store.Global_Status[('Strategy'+ StrategyNo)].append(("StopLoss is CE: "+ str(round(Store.stopLoss[StrategyNo]['CE'],2)) + ' PE: '  +  str(round(Store.stopLoss[StrategyNo]['PE'],2))))
            Quantity = 75 
            exchange = 'NFO'
            
            orderIDPE= TradeAPI.place_order(variety=TradeAPI.VARIETY_REGULAR,
                                            tradingsymbol=Store.ZerodhaStrike[StrategyNo]['PE'],
                                            exchange=exchange,
                                        transaction_type=TradeAPI.TRANSACTION_TYPE_BUY,
                                            quantity=Quantity,
                                            order_type=TradeAPI.ORDER_TYPE_SL,
                                            price=math.ceil(Store.stopLoss[StrategyNo]["PE"])+5,
                                            trigger_price=math.ceil(Store.stopLoss[StrategyNo]["PE"]),
                                            product="NRML",
                                            validity=TradeAPI.VALIDITY_DAY)
            orderIDCE = TradeAPI.place_order(variety=TradeAPI.VARIETY_REGULAR,
                                            tradingsymbol=Store.ZerodhaStrike[StrategyNo]['CE'],
                                            exchange=exchange,
                                        transaction_type=TradeAPI.TRANSACTION_TYPE_BUY,
                                            quantity=Quantity,
                                            order_type=TradeAPI.ORDER_TYPE_SL,
                                            price=math.ceil(Store.stopLoss[StrategyNo]["CE"])+5,
                                            trigger_price=math.ceil(Store.stopLoss[StrategyNo]["CE"]),
                                            product="NRML",
                                            validity=TradeAPI.VALIDITY_DAY)
            print(orderIDCE , orderIDPE)
            while(True):
                CEOrderHistory = TradeAPI.order_history(orderIDCE)
                PEOrderHistory = TradeAPI.order_history(orderIDPE)
                # print(CEOrderHistory[-1]['status'])
                print("CE: ",CEOrderHistory[-1]['status'])
                print("PE: ",PEOrderHistory[-1]['status'])
                if CEOrderHistory[-1]['status']=="COMPLETE":
                    try:
                      TradeAPI.cancel_order(TradeAPI.VARIETY_REGULAR  , orderIDPE , parent_order_id=None)
                      orderID= TradeAPI.place_order(variety=TradeAPI.VARIETY_REGULAR,
                                            tradingsymbol=Store.ZerodhaStrike[StrategyNo]['CE'],
                                            exchange=exchange,
                                            transaction_type=TradeAPI.TRANSACTION_TYPE_SELL,
                                            quantity=Quantity,
                                            order_type=TradeAPI.ORDER_TYPE_LIMIT,
                                            product="NRML",
                                            price = math.ceil(Store.Price[StrategyNo]['CE'])*2,
                                            validity=TradeAPI.VALIDITY_DAY)
                      print('placed')
                      while (True):
                         ltp = (TradeAPI.ltp(exchange+":"+ Store.ZerodhaStrike[StrategyNo]['PE'])).get(exchange+":"+ Store.ZerodhaStrike[StrategyNo]['PE']).get('last_price')
                         if ltp >= Store.Price[StrategyNo]['PE']:
                            TradeAPI.modify_order( variety=TradeAPI.VARIETY_REGULAR, order_id= orderID , order_type=TradeAPI.ORDER_TYPE_MARKET )

                    except Exception as e:
                        print(e)
                        print(math.ceil(Store.Price[StrategyNo]['CE'])*2)
                        
                        
                    break
                if PEOrderHistory[-1]['status']=="COMPLETE":
                    try:
                      TradeAPI.cancel_order(TradeAPI.VARIETY_REGULAR , orderIDCE , parent_order_id=None)
  
                      orderID= TradeAPI.place_order(variety=TradeAPI.VARIETY_REGULAR,
                                            tradingsymbol=Store.ZerodhaStrike[StrategyNo]['PE'],
                                            exchange=exchange,
                                            transaction_type=TradeAPI.TRANSACTION_TYPE_SELL,
                                            quantity=Quantity,
                                            order_type=TradeAPI.ORDER_TYPE_LIMIT,
                                            product="NRML",
                                            price = math.ceil(Store.Price[StrategyNo]['PE'])*2,
                                            validity=TradeAPI.VALIDITY_DAY)
                      print('placed')
                      while (True):
                         ltp = (TradeAPI.ltp(exchange+":"+ Store.ZerodhaStrike[StrategyNo]['CE'])).get(exchange+":"+ Store.ZerodhaStrike[StrategyNo]['CE']).get('last_price')
                         if ltp >= Store.Price[StrategyNo]['CE']:
                            TradeAPI.modify_order( variety=TradeAPI.VARIETY_REGULAR, order_id= orderID , order_type=TradeAPI.ORDER_TYPE_MARKET )

                    except Exception as e:
                        print(e)
                        print(math.ceil(Store.Price[StrategyNo]['PE'])*2)
                    break
                
                time.sleep(1)
                os.system('clear')
        

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        # print("Exiting Code!!!")
        Store.Global_Status[('Strategy'+ StrategyNo)].append('Error in code , there for ended ' +" " + str(exc_type) +" " + str (fname)+" " +str (exc_tb.tb_lineno) +" " + str(e) )

        return False 
    else:
    
        Store.status1[StrategyNo] = Store.Trading_Strategy_Started
        Store.Global_Status[('Strategy'+ StrategyNo)].append('Trading_Strategy_Started Successfully')

        TradeFunctionStart=  Execute.sl(ApiZerodha , Variables,QuantityJSON , Cred , TradeFunctionStart, StrategyNo ,   )

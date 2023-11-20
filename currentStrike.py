
import math


def currentStrike(api , index , ltp , formatted_time, endDate, time ):
#     print(ltp)  
    if ltp ==0:  
      atmStrike =0
      if(index =="BANKNIFTY"):
            ltp = (api.ltp('NSE:NIFTY BANK')).get('NSE:NIFTY BANK').get('last_price')
            mod = int(ltp) % 100
            if mod < 50:
                  atmStrike = int(math.floor(ltp/100))*100
            else:
                  atmStrike = int(math.ceil(ltp/100))*100

      elif(index =="NIFTY"):   
            ltp = ltp = (api.ltp('NSE:NIFTY 50')).get('NSE:NIFTY 50').get('last_price')

            mod = int(ltp) % 50
            if mod < 25:
                  atmStrike = int(math.floor(ltp/50))*50
            else:
                  atmStrike = int(math.ceil(ltp/50))*50

      elif(index =="FINNIFTY"):   
            ltp = (api.ltp('NSE:NIFTY FIN SERVICE')).get('NSE:NIFTY FIN SERVICE').get('last_price')

            mod = int(ltp) % 50
            if mod < 25:
                  atmStrike = int(math.floor(ltp/50))*50
            else:
                  atmStrike = int(math.ceil(ltp/50))*50
      elif(index =="SENSEX"):   
            ltp = (api.ltp('BSE:SENSEX')).get('BSE:SENSEX').get('last_price')

            mod = int(ltp) % 100
            if mod < 50:
                  atmStrike = int(math.floor(ltp/100))*100
            else:
                  atmStrike = int(math.ceil(ltp/100))*100
      
      elif(index =="MIDCPNIFTY"):   
            ltp = (api.ltp('NSE:NIFTY MID SELECT')).get('NSE:NIFTY MID SELECT').get('last_price')

            mod = int(ltp) % 25
            if mod < 12.5:
                  atmStrike = int(math.floor(ltp/25))*25
            else:
                  atmStrike = int(math.ceil(ltp/25))*25

      return atmStrike
      
    else :
            
      if(index =="BANKNIFTY"):
            ltp = (api.ltp('NSE:NIFTY BANK')).get('NSE:NIFTY BANK')
            ltp = (api.historical_data(ltp.get('instrument_token'), formatted_time, endDate, '5minute', continuous=False, oi=False))[time].get('open')

            mod = int(ltp) % 100
            if mod < 50:
                  atmStrike = int(math.floor(ltp/100))*100
            else:
                  atmStrike = int(math.ceil(ltp/100))*100

      elif(index =="NIFTY"):   
            ltp  = (api.ltp('NSE:NIFTY 50')).get('NSE:NIFTY 50')
            ltp = (api.historical_data(ltp.get('instrument_token'), formatted_time, endDate, '5minute', continuous=False, oi=False))[time].get('open')
           


            mod = int(ltp) % 50
            if mod < 25:
                  atmStrike = int(math.floor(ltp/50))*50
            else:
                  atmStrike = int(math.ceil(ltp/50))*50

      elif(index =="FINNIFTY"):   
            ltp = (api.ltp('NSE:NIFTY FIN SERVICE')).get('NSE:NIFTY FIN SERVICE')
            ltp = (api.historical_data(ltp.get('instrument_token'), formatted_time, endDate, '5minute', continuous=False, oi=False))[time].get('open')

            mod = int(ltp) % 50
            if mod < 25:
                  atmStrike = int(math.floor(ltp/50))*50
            else:
                  atmStrike = int(math.ceil(ltp/50))*50
      elif(index =="SENSEX"):   
            ltp = (api.ltp('BSE:SENSEX')).get('BSE:SENSEX')
            ltp = (api.historical_data(ltp.get('instrument_token'), formatted_time, endDate, '5minute', continuous=False, oi=False))[time].get('open')
            print(ltp)
            mod = int(ltp) % 100
            if mod < 50:
                  atmStrike = int(math.floor(ltp/100))*100
            else:
                  atmStrike = int(math.ceil(ltp/100))*100
      
      elif(index =="MIDCPNIFTY"):   
            ltp = (api.ltp('NSE:NIFTY MID SELECT')).get('NSE:NIFTY MID SELECT')
            ltp = (api.historical_data(ltp.get('instrument_token'), formatted_time, endDate, '5minute', continuous=False, oi=False))[time].get('open')

            print(ltp)
            mod = int(ltp) % 25
            if mod < 12.5:
                  atmStrike = int(math.floor(ltp/25))*25
            else:
                  atmStrike = int(math.ceil(ltp/25))*25
            print(atmStrike)
      return atmStrike
      
      
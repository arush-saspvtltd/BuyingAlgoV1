from Login_Zerodha import login_in_zerodha
from kiteconnect import KiteConnect
from GenerateBasket import GenerateBasket
from Store.Strategies import Strategies
import json , os , time , requests,datetime , threading , sys
from Functions import Store  , Script , ExtraFunctions 
from Store import Cred
import pandas as pd
ZerodhaApis = []

ZerodhaAccounts = []

global TradeFunctionStart

def wait_until_valid_time():
    start_time = datetime.time(8, 45, 0)
    end_time = datetime.time(15, 30, 0)

    while True:
        current_time = datetime.datetime.now().time()

        if start_time <= current_time <= end_time:
            print("The current time is within the specified range. Continuing with the program.")
            break

        print(f"Waiting for valid time. Current time: {current_time}")
        time.sleep(5)  # Wait for 1 minute before checking again

# Call the function to start waiting
wait_until_valid_time()

# Your program logic goes here
print("Program is now running.")



def addZerodhaAccount(Credentials):
    ZerodhaAccounts.append(Credentials)

addZerodhaAccount(Cred.Crosshair)
# addZerodhaAccount(Cred.Riyaaz)
# addZerodhaAccount(Cred.Harsh2)
# addZerodhaAccount(Cred.Sanjay)
# addZerodhaAccount(Cred.AnkitShah)
# addZerodhaAccount(Cred.Parag)
# addZerodhaAccount(Cred.Ankit)
# addZerodhaAccount(Cred.Manjunath)
# addZerodhaAccount(Cred.Milan)
# addZerodhaAccount(Cred.Rishee)
# addZerodhaAccount(Cred.Sumit)
# addZerodhaAccount(Cred.InjoNavish)
# addZerodhaAccount(Cred.Vijet)
# addZerodhaAccount(Cred.Dilip)


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




#  Generate Basket
if not ExtraFunctions.is_function_used_today("GenerateBasket"):
 QuantityJSON = GenerateBasket(ZerodhaApis)
 with open("Logs/GenerateBasket.txt", "a") as file:
              file.write(str(datetime.date.today()) + "\n")

with open("Quantity.json") as f:
         QuantityJSON = json.load(f)
         
for Client in QuantityJSON:
    
    QuantityJSON[Client]["API"] =  ExtraFunctions.ZerodhaApiLogin(QuantityJSON[Client]["Cred"])['API']


Day = datetime.datetime.now().isoweekday()
# Day = 4
# MainAPI = ExtraFunctions.ZerodhaApiLogin(Cred.Crosshair)
MainAPI = ExtraFunctions.ZerodhaApiLogin(Cred.Harsh2)


    
def TradeFunction(Variables  , StrategyNo):
    Store.status[StrategyNo] = "Function " + StrategyNo + " has Started"
    Variables['StrategyName'] = StrategyNo
    TradeFunctionStart = True 
    Store.Global_Status[('Strategy'+ StrategyNo)] = []
    Store.Global_Status[('Strategy'+ StrategyNo)].append('TradeFunction has Started')
    while TradeFunctionStart:
      
    #   os.system('clear')
      if ExtraFunctions.CompareTime(Variables['Time']):
        time.sleep(5)
        
        with open("Logs/" + StrategyNo + ".txt", "a") as file:
            # file.write(str(datetime.date.today()) + "\n")
            ExtraFunctions.send_to_telegram("Started taking Trade")
            Store.Global_Status[('Strategy'+ StrategyNo)].append('Time Requirement Fulfilled')

        TradeFunctionStart = Script.Search(MainAPI["API"]  , Variables ,  QuantityJSON , Cred.Harsh2 , TradeFunctionStart, StrategyNo)
        


if  ExtraFunctions.is_function_used_today("1") == False:
    
    threading.Thread(target=TradeFunction ,args = [Strategies[str(Day)]['1'] , "1"]).start()
else :
    print("Main One has Finished")
    
if  ExtraFunctions.is_function_used_today("2") == False:
    
    threading.Thread(target=TradeFunction ,args = [Strategies[str(Day)]['2'] , "2"]).start()
else :
    print("Main Two has Finished")
if  ExtraFunctions.is_function_used_today("3") == False:
    
    threading.Thread(target=TradeFunction ,args = [Strategies[str(Day)]['3'] , "3"]).start()
else :
    print("Main Three has Finished")
if  ExtraFunctions.is_function_used_today("4") == False:
    
    threading.Thread(target=TradeFunction ,args = [Strategies[str(Day)]['4'] , "4"]).start()
else :
    print("Main Four has Finished")
    
while True :
    # try :
        # print((Store.Global_Status))
        print( "Time:", datetime.datetime.now().strftime('%H:%M:%S'))
        ExtraFunctions.display_arrays_and_objects(Store.Global_Status)
        
        
    # except Exception as  e:
    #     print(e , "Exception in main") 
        time.sleep(1)
        os.system('clear')

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

addZerodhaAccount(Cred.Crosshair2)
# addZerodhaAccount(Cred.Riyaaz)
addZerodhaAccount(Cred.Harsh2)
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
MainAPI = ExtraFunctions.ZerodhaApiLogin(Cred.Harsh2)
TradeAPI = ExtraFunctions.ZerodhaApiLogin(Cred.Crosshair2)

while (True):
    ltp= TradeAPI['API'].ltp("BFO:SENSEX24AUG82400CE" )
    print(ltp)

import sys
sys.path.append(r"")

from NorenRestApiPy.NorenApi import  NorenApi
import pyotp
from datetime import datetime as dt
from datetime import timedelta as td
from Functions import Cred

            

api = None

def ConnectApi(Cred):
    global api

    try:
        class ShoonyaApiPy(NorenApi):
            def __init__(self):
                NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/', eodhost='https://api.shoonya.com/chartApi/getdata/')
                
        api = ShoonyaApiPy()
    except Exception as e:
        class ShoonyaApiPy(NorenApi):
            def __init__(self):
                NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')
                
        api = ShoonyaApiPy()
        pass
    
    login_status = api.login(userid=Cred["user"], password=Cred["pwd"], twoFA=pyotp.TOTP(Cred["factor2"]).now(),
                             vendor_code=Cred["vc"], api_secret=Cred["app_key"], imei=Cred["imei"])
    print(login_status)
    
    #print(f"login_status = {login_status}")
    f=open("Login/" +str(Cred["user"])+'.txt','w')
    f.write(login_status.get('susertoken'))
    f.close()

    login_status = login_status.get('uname') + " " + login_status.get('stat') + " token = " + login_status.get('susertoken')
    print(login_status)
    


ConnectApi(Cred.Parag)


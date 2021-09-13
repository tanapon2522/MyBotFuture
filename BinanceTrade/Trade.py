from binance.client import Client
from BinanceTrade.FutureTrade import *

try : 
    from config_dev import API_BINANCE_KEY , API_BINANCE_SECRET
except Exception:
    from config_prod import API_BINANCE_KEY , API_BINANCE_SECRET

from DB.Firebasedb import GetDataBotSetting , UpdateBotSetting

client = Client( API_BINANCE_KEY , API_BINANCE_SECRET )

def ReceiveSignals(signal_data_dict):

    """
    Data
    {
        "message" : "CLOSE LONG", ---> CLOSE or OPEN / LONG or SHORT
        "symbol" : "BTCUSDT"
    }
    """
    Signal_Type = signal_data_dict["message"].split(" ")[0]
    Signal_Side = signal_data_dict["message"].split(" ")[1]
    Signal_Symbol = signal_data_dict["symbol"]

    msg = ""

    amount = float(GetDataBotSetting(key="Positionsize"))
    lev = float(GetDataBotSetting(key="Lev"))
    cshort = GetDataBotSetting(key="CShort")
    clong = GetDataBotSetting(key="CLong")


    if Signal_Type == "OPEN":
        if getPositionbySymbol(Signal_Symbol)['positionAmt'] == 0 :
            if (Signal_Side == "SHORT") and not (cshort):
                UpdateBotSetting(key="CShort",value=True)
                cshort = GetDataBotSetting(key="CShort")
            elif (Signal_Side == "LONG") and not (clong):        
                UpdateBotSetting(key="CLong",value=True)
                clong = GetDataBotSetting(key="CLong")
            try :
                CancelAllOrder(symbol = Signal_Symbol) 
            except Exception as e :
                print(e.error_message)
                
        if (Signal_Side == "SHORT") and (cshort):
            try :
                ClosePositionAtmarket(symbol=Signal_Symbol, positionSide="LONG")
            except Exception as e :
                print(e.error_message)
            PlaceOrderAtMarket(position=Signal_Side, symbol=Signal_Symbol, amount=amount, lev = lev)
            msg = "ทำการ {} Position ในฝั่ง {} คู่สินค้า {} ".format(Signal_Type,Signal_Side,Signal_Symbol)   
            
        elif (Signal_Side == "LONG") and (clong):
            try :
                ClosePositionAtmarket(symbol=Signal_Symbol, positionSide="SHORT")
            except Exception as e :
                print(e.error_message)
            PlaceOrderAtMarket(position=Signal_Side, symbol=Signal_Symbol, amount=amount, lev = lev)
            msg = "ทำการ {} Position ในฝั่ง {} คู่สินค้า {} ".format(Signal_Type,Signal_Side,Signal_Symbol)
        
            
    elif Signal_Type == "CLOSE":
        if getPositionbySymbol(Signal_Symbol)['positionAmt'] == 0 :
            if (Signal_Side == "SHORT") and not (cshort):
                UpdateBotSetting(key="CShort",value=True)
                cshort = GetDataBotSetting(key="CShort")

            elif (Signal_Side == "LONG") and not (clong):    
                UpdateBotSetting(key="CLong",value=True)
                clong = GetDataBotSetting(key="CLong")
        

        if (Signal_Side == "SHORT") and not (cshort):
            try :
                ClosePositionAtmarket(symbol=Signal_Symbol, positionSide=Signal_Side)            
            except Exception as e :
                    print(e.error_message)
            msg = "ทำการ {} Position ในฝั่ง {} คู่สินค้า {} ".format(Signal_Type,Signal_Side,Signal_Symbol)
        elif (Signal_Side == "LONG") and not (clong):
            try :
                ClosePositionAtmarket(symbol=Signal_Symbol, positionSide=Signal_Side)            
            except Exception as e :
                    print(e.error_message)
            msg = "ทำการ {} Position ในฝั่ง {} คู่สินค้า {} ".format(Signal_Type,Signal_Side,Signal_Symbol)
            
    return msg


from binance.client import Client
from BinanceTrade.FutureTrade import *

try : 
    from config_dev import API_BINANCE_KEY , API_BINANCE_SECRET
except Exception:
    from config_prod import API_BINANCE_KEY , API_BINANCE_SECRET

from DB.Firebasedb import GetDataBotSetting

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

    if Signal_Type == "OPEN":
        PlaceOrderAtMarket(position=Signal_Side, symbol=Signal_Symbol, amount=20)
        msg = "ทำการ {} Position ในฝั่ง {} คู่สินค้า {} ".format(Signal_Type,Signal_Side,Signal_Symbol)

    elif Signal_Type == "CLOSE":
        ClosePositionAtmarket(symbol=Signal_Symbol, positionSide=Signal_Side)
        msg = "ทำการ {} Position ในฝั่ง {} คู่สินค้า {} ".format(Signal_Type,Signal_Side,Signal_Symbol)
        
    return msg


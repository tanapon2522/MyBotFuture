from BinanceTrade.FutureTrade import *
from BinanceTrade.Trade import ReceiveSignals
import json

from line.notify import sendmsg
from DB.Firebasedb import GetDataBotSetting , UpdateBotSetting


if __name__ == "__main__":


    json_msg = {
        "message":"OPEN SHORT",
        "symbol":"SRMUSDT"
        }
    msg = ReceiveSignals(signal_data_dict = json_msg )

    clong =GetDataBotSetting(key="CLong")
    cshort =GetDataBotSetting(key="CShort")
    Signal_Type = json_msg["message"].split(" ")[0]
    Signal_Side = json_msg["message"].split(" ")[1]

    if Signal_Type == "OPEN":
        if (Signal_Side=="LONG") and clong:
            sendmsg(msg=json.dumps(json_msg))
            sendmsg(msg=msg)
            UpdateBotSetting(key="CLong",value=False)
            UpdateBotSetting(key="CShort",value=True)
        elif (Signal_Side=="SHORT") and cshort:
            sendmsg(msg=json.dumps(json_msg))
            sendmsg(msg=msg)
            UpdateBotSetting(key="CShort",value=False)
            UpdateBotSetting(key="CLong",value=True)
    elif Signal_Type == "CLOSE":
        if (Signal_Side=="LONG") and not clong:
            sendmsg(msg=json.dumps(json_msg))
            sendmsg(msg=msg)
            UpdateBotSetting(key="CLong",value=True)
            
        elif (Signal_Side=="SHORT") and not cshort:
            sendmsg(msg=json.dumps(json_msg))
            sendmsg(msg=msg)
            UpdateBotSetting(key="CShort",value=True)            
    print(msg)

    # from line.notify import notify
    # notify.send("TESTFUTURE")

    # res = get_market_data_by_symbol(symbol="BTCUSDT")
    # print(res["markPrice"])

    #change_leverage(symbol="BTCUSDT",lev=15)

    # balance = getAssetUSDT()
    # print(balance)

    # PlaceOrderAtMarket(
    #     position='SHORT',         
    #     symbol='SOLUSDT',      
    # )

    #res = getPositionbySymbol(Symbol="RAYUSDT")
    #print(res)
    # print(res['positionAmt'])

    # ClosePositionAtmarket(symbol="BTCUSDT", positionSide="SHORT")


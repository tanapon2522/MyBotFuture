from BinanceTrade.FutureTrade import *
from BinanceTrade.Trade import ReceiveSignals

if __name__ == "__main__":


    # data = {
    #     "message":"CLOSE LONG",
    #     "symbol":"BTCUSDT"
    #     }
    # msg = ReceiveSignals(signal_data_dict = data )
    # print(msg)

    from line.notify import notify
    notify.send("TESTFUTURE")

    # res = get_market_data_by_symbol(symbol="BTCUSDT")
    # print(res["markPrice"])

    #change_leverage(symbol="BTCUSDT",lev=15)

    # balance = getAssetUSDT()
    # print(balance)

    # PlaceOrderAtMarket(
    #     position='SHORT',         
    #     symbol='SOLUSDT', 
    #     amount=20
    # )

    # res = getPositionbySymbol(Symbol="BTCUSDT")
    # print(res['positionAmt'])

    # ClosePositionAtmarket(symbol="BTCUSDT", positionSide="SHORT")


from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

import math #< แก้ไข 6-27-2021

try:
    from config_dev import API_BINANCE_KEY , API_BINANCE_SECRET
except:
    from config_prod import API_BINANCE_KEY , API_BINANCE_SECRET

request_client = RequestClient(api_key=API_BINANCE_KEY,secret_key=API_BINANCE_SECRET)


def get_market_data_by_symbol(symbol):
    result = request_client.get_mark_price(symbol=symbol)
    return result.__dict__

def change_leverage(symbol,lev):
    result = request_client.change_initial_leverage(symbol,lev)
    return result.__dict__

def CancelAllOrder(symbol):
    result = request_client.cancel_all_orders(symbol)
    return result.__dict__

def getAssetUSDT():
    result = request_client.get_balance()
    return int(result[1].balance)

#< แก้ไข เพิ่ม function 6-27-2021
def PlaceOrderAtMarket(position,symbol,amount,lev,act_price_percent=0.1,cb=1,stoploss_Percent = 1):
    """
    UPDATE LOGIC 6-27-2021 (ดูวิดิโอในกลุ่ม)
    position : Long or Short
    amount : จำนวน USDT ที่ต้องการใช้ในการซื้อ
    """

    CancelAllOrder(symbol = symbol)
    current_price = float(get_market_data_by_symbol(symbol)["markPrice"])
    amount = (amount* lev)/current_price
    change_leverage(symbol=symbol,lev=lev)

    if position == "LONG":        
        act_price_LONG = float(current_price * (1 + act_price_percent/100))
        stoplosePrice = float(current_price * (1 - stoploss_Percent/100))

        POS_SIZE = str(amount)
            
        Interger = POS_SIZE.split(".")[0]
        decimal = POS_SIZE.split(".")[1]
        
        dec_count = -1

        # While loop เนื่องจาก เราจะต้องทำคำสั่งจนกว่าจะสำเร็จ ซึ่งสินค้าแต่ละประเภทอาจมี ทศนิยม ที่ต่างกัน
        # แอดมินแนะนำให้ทำแบบ การซื้อขาย Course 2 ที่สอนไปนะครับ แยกจำนวนเต็ม และ ทศนิยม แล้ว ค่อยๆตัดทศนิยม
        
        while True:
            if float(amount) > 0 :
                try:
                    # buy order at market
                    result = request_client.post_order(
                        symbol = symbol ,
                        side = OrderSide.BUY ,
                        positionSide = "BOTH" ,
                        ordertype=OrderType.MARKET ,
                        quantity = amount # 0.02 --> 0.019999999
                    )
                    # break ออกจาก loop ถ้าหาก เนื่องจากทำคำสั่งสำเร็จ
                    break
                except Exception as e: # ตรวจจับว่า เป้นกรณี code -1111 คือ ทศนิยมผิดพลาดหรือไม่ ลองไปทดสอบดูนะครับ
                    print(e.error_message)
                    #ลอง print(e) แล้วเช็คกรณี error code -1111 นะครับ
                    amount = Interger + "." + decimal[:dec_count]                    
                    if decimal[:dec_count] == "":
                        amount = int(Interger)
                        print("amount lower")
                    dec_count = dec_count - 1

        
        POS_SIZE = str(act_price_LONG)
            
        Interger = POS_SIZE.split(".")[0]
        decimal = POS_SIZE.split(".")[1]
        dec_count = -1

        while True :        
            if float(act_price_LONG) > 0 :
                try :
                    # trailing stop loss ควรทำแบบ While loop ด้านบนเช่นกัน
                    result = request_client.post_order(
                        symbol = symbol ,
                        side = OrderSide.SELL ,
                        positionSide = "BOTH" ,
                        ordertype = OrderType.TRAILING_STOP_MARKET,
                        activationPrice=act_price_LONG,
                        callbackRate= cb,
                        reduceOnly = True ,
                        quantity = amount
                    )
                    # break ออกจาก loop ถ้าหาก เนื่องจากทำคำสั่งสำเร็จ
                    break
                except Exception as e: # ตรวจจับว่า เป้นกรณี code -1111 คือ ทศนิยมผิดพลาดหรือไม่ ลองไปทดสอบดูนะครับ
                    print(e.error_message)
                    #ลอง print(e) แล้วเช็คกรณี error code -1111 นะครับ                    
                    act_price_LONG = Interger + "." + decimal[:dec_count]
                    if decimal[:dec_count] == "":
                        act_price_LONG = int(Interger)
                    dec_count = dec_count - 1 
                        

        
        POS_SIZE = str(stoplosePrice)
            
        Interger = POS_SIZE.split(".")[0]
        decimal = POS_SIZE.split(".")[1]
        dec_count = -1 

        while True :
            if float(stoplosePrice) > 0 :
                try :
                    # Initial Stoploss ควรทำแบบ While loop ด้านบนเช่นกัน                
                    result = request_client.post_order(
                        symbol = symbol ,
                        side = OrderSide.SELL ,
                        positionSide = "BOTH" ,
                        ordertype = OrderType.STOP_MARKET,
                        stopPrice = stoplosePrice,
                        reduceOnly=True,
                        quantity = amount
                    )
                    break
                except Exception as e: # ตรวจจับว่า เป้นกรณี code -1111 คือ ทศนิยมผิดพลาดหรือไม่ ลองไปทดสอบดูนะครับ
                    print(e.error_message)
                    #ลอง print(e) แล้วเช็คกรณี error code -1111 นะครับ
                    stoplosePrice = Interger + "." + decimal[:dec_count]                    
                    if decimal[:dec_count] == "":
                        stoplosePrice = int(Interger)
                    dec_count = dec_count - 1 

    if position == "SHORT":
        act_price_SHORT = float(current_price * (1 - act_price_percent/100))
        stoplosePrice = float(current_price * (1 + stoploss_Percent/100))

        POS_SIZE = str(amount)
            
        Interger = POS_SIZE.split(".")[0]
        decimal = POS_SIZE.split(".")[1]
        dec_count = -1

        # While loop เนื่องจาก เราจะต้องทำคำสั่งจนกว่าจะสำเร็จ ซึ่งสินค้าแต่ละประเภทอาจมี ทศนิยม ที่ต่างกัน
        # แอดมินแนะนำให้ทำแบบ การซื้อขาย Course 2 ที่สอนไปนะครับ แยกจำนวนเต็ม และ ทศนิยม แล้ว ค่อยๆตัดทศนิยม
            
        while True:
            if float(amount) > 0 :
                try:
                    # buy order at market
                    result = request_client.post_order(
                        symbol = symbol ,
                        side = OrderSide.SELL ,
                        positionSide = "BOTH" ,
                        ordertype=OrderType.MARKET ,
                        quantity = amount # 0.02 --> 0.019999999
                    )
                    # break ออกจาก loop ถ้าหาก เนื่องจากทำคำสั่งสำเร็จ
                    break

                except Exception as e: # ตรวจจับว่า เป้นกรณี code -1111 คือ ทศนิยมผิดพลาดหรือไม่ ลองไปทดสอบดูนะครับ
                    print(e.error_message)
                    #ลอง print(e) แล้วเช็คกรณี error code -1111 นะครับ
                    amount = Interger + "." + decimal[:dec_count]                    
                    if decimal[:dec_count] == "":
                        amount = int(Interger)
                        print("amount lower")
                    dec_count = dec_count - 1

        POS_SIZE = str(act_price_SHORT)
            
        Interger = POS_SIZE.split(".")[0]
        decimal = POS_SIZE.split(".")[1]
        dec_count = -1

        while True :
            if float(act_price_SHORT) > 0 :
                try :
                    # trailing stop loss ควรทำแบบ While loop ด้านบนเช่นกัน
                    result = request_client.post_order(
                        symbol = symbol ,
                        side = OrderSide.BUY ,
                        positionSide = "BOTH" ,
                        ordertype = OrderType.TRAILING_STOP_MARKET,
                        activationPrice=act_price_SHORT,
                        callbackRate= cb,
                        reduceOnly = True ,
                        quantity = amount
                    )
                    # break ออกจาก loop ถ้าหาก เนื่องจากทำคำสั่งสำเร็จ
                    break
                except Exception as e: # ตรวจจับว่า เป้นกรณี code -1111 คือ ทศนิยมผิดพลาดหรือไม่ ลองไปทดสอบดูนะครับ
                    print(e.error_message)
                    #ลอง print(e) แล้วเช็คกรณี error code -1111 นะครับ                    
                    act_price_SHORT = Interger + "." + decimal[:dec_count]
                    if decimal[:dec_count] == "":
                        act_price_SHORT = int(Interger)
                    dec_count = dec_count - 1 
                    
        POS_SIZE = str(stoplosePrice)
            
        Interger = POS_SIZE.split(".")[0]
        decimal = POS_SIZE.split(".")[1]
        dec_count = -1 

        while True :
            if float(stoplosePrice) > 0 :
                try :
                    # Initial Stoploss ควรทำแบบ While loop ด้านบนเช่นกัน
                    result = request_client.post_order(
                        symbol = symbol ,
                        side = OrderSide.BUY ,
                        positionSide = "BOTH" ,
                        ordertype = OrderType.STOP_MARKET,
                        stopPrice = float(stoplosePrice),
                        reduceOnly=True,
                        quantity = amount
                    )
                    break
                except Exception as e: # ตรวจจับว่า เป้นกรณี code -1111 คือ ทศนิยมผิดพลาดหรือไม่ ลองไปทดสอบดูนะครับ
                    print(e.error_message)
                    #ลอง print(e) แล้วเช็คกรณี error code -1111 นะครับ
                    stoplosePrice = Interger + "." + decimal[:dec_count]                    
                    if decimal[:dec_count] == "":
                        stoplosePrice = int(Interger)
                    dec_count = dec_count - 1 
                    
def getPositionbySymbol(Symbol):
    result = request_client.get_position_v2()
    for i in result:
        if i.symbol == Symbol:
            return i.__dict__

def ClosePositionAtmarket(symbol,positionSide):

    amount = getPositionbySymbol(symbol)['positionAmt']

    if positionSide == "LONG":
        result = request_client.post_order(
            symbol=symbol,
            side=OrderSide.SELL, 
            ordertype=OrderType.MARKET,
            positionSide="BOTH",
            quantity=str(abs(float(amount)))
        )

    elif positionSide == "SHORT":
        result = request_client.post_order(
            symbol=symbol,
            side=OrderSide.BUY, 
            ordertype=OrderType.MARKET,
            positionSide="BOTH",
            quantity=str(abs(float(amount)))
        )


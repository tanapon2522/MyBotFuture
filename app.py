from flask import Flask , request
import json

from BinanceTrade.Trade import ReceiveSignals
from line.notify import sendmsg
from DB.Firebasedb import GetDataBotSetting , UpdateBotSetting

app = Flask(__name__)

#@app.route("/START/REBALANCEBOT/SYMBOL")

#@app.route("/STOP/REBALANCEBOT/SYMBOL")

@app.route("/SIGNALS" , methods=['POST'])
def SIGNALS_RECEIVER():
    if request.method == "POST":
        msg = request.data.decode("utf-8")
        json_msg = json.loads(msg)
        print(json_msg) # <-- dictionary

        if GetDataBotSetting(key="run") == True:
            # get data firebase เพื่อดูว่า Autotrading = True??
            msg = ReceiveSignals(signal_data_dict = json_msg)
        
        clong =GetDataBotSetting(key="CLong")
        cshort =GetDataBotSetting(key="CShort")

        if (json_msg["SIGNALS"]=="LONG") and clong:
            UpdateBotSetting(key="CShort",value=True)
            UpdateBotSetting(key="CLong",value=False)
            sendmsg(msg=json.dumps(json_msg))
            sendmsg(msg=msg)
        elif (json_msg["SIGNALS"]=="SHORT") and cshort:
            UpdateBotSetting(key="CShort",value=False)
            UpdateBotSetting(key="CLong",value=True)
            sendmsg(msg=json.dumps(json_msg))
            sendmsg(msg=msg)

        # สร้างฟังก์ชั่น ในการจัดการข้อมูล

        # """
        # { "SYMBOL":"{{TICKER}}",
        # "TIME":{{timenow}},
        # "SIGNALS":"{{strategy.order.action}}",
        # "POSITION_SIZE":{{strategy.order.contracts}} }

        # example data

        # { "SYMBOL":"BTCUSD",
        # "TIME":TIMESTAMP,
        # "SIGNALS":"buy",
        # "POSITION_SIZE":0.34 }
        # """
    return "200"

from line.LineBot import handler

@app.route("/linebot", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

if __name__== "__main__":
    app.run(debug=True,port=8080)
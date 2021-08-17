import os
API_BINANCE_KEY = os.getenv("API_BINANCE_KEY")
API_BINANCE_SECRET = os.getenv("API_BINANCE_SECRET")

API_LINE_KEY = os.getenv("API_LINE_KEY")
API_CLIENT_SECRET = os.getenv("API_CLIENT_SECRET")
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

LINE_BOT_ACCESS_TOKEN = os.getenv("LINE_BOT_ACCESS_TOKEN")
LINE_BOK_CHANNAL_SECRET = os.getenv("LINE_BOK_CHANNAL_SECRET")

from firebase import Firebase

firebaseConfig = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": "bottrade-db-mybot.firebaseapp.com",
    "projectId": "bottrade-db-mybot",
    "storageBucket": "bottrade-db-mybot.appspot.com",
    "messagingSenderId": "415126488514",
    "appId": "1:415126488514:web:6964274a970b76ad38025b",
    "measurementId": "G-6NB6B7B2NP",
    "databaseURL": os.getenv("FirebaseDatabaseURL"),
    "serviceAccount" : "bottrade-db-mybot-firebase-adminsdk-d1hnd-36975cb408.json" # นำไฟล์ของท่านมาใส่เองด้วย
  }

firebaseClient = Firebase(firebaseConfig)
auth = firebaseClient.auth()
user = auth.sign_in_with_email_and_password(os.getenv("FIREBASE_EMAIL"),os.getenv("FIREBASE_PASSWORD"))

#ทดสอบ
if __name__ == '__main__':
  db = firebaseClient.database()
  data = {
    "name":"TEST"
  }
  user = auth.refresh(user['refreshToken'])
  results = db.child("users").push(data, user['idToken'])
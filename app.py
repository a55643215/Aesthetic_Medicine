from flask import Flask,request,abort
from events.service import *
from line_bot_api import *
from events.basic import *

from extensions import db, migrate
from models.user import User
import os

app = Flask(__name__)#admin: !QAZ2wsx資料庫的帳號和密碼
#讓程式自己去判斷如果是測試端就會使用APP_SETTINGS
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://doctordb:X1rooPEa77V2nfQlhH5OwwzVlx6WNt9n@dpg-cjbikn45kgrc73a7of9g-a.singapore-postgres.render.com/doctordb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)


#callback

@app.route("/callback", methods=['POST'])
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

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()

    if message_text == '@關於我們':
        about_us_event(event)

    elif message_text == '@營業據點':
        location_event(event)
    elif message_text =='@預約服務':
        service_catgory_event(event)


#接收postback的訊息
#parse_qsl解析data中的資料
@handler.add(PostbackEvent)
def handle_postback(event):
    #把傳進來的event儲存在postback.data中再利用parse_qsl解析data中的資料然漚轉換成dict
    data = dict(parse_qsl(event.postback.data))
    #建立好def service_event(event) function後要來這裡加上判斷式
    #直接呼叫service_event(event)

    if data.get('action') == 'service':
        service_event(event)


################## 解除封鎖 ####################
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg="""Hello! 您好，歡迎您成為 CHIEN Doctor 的好友！

我是 CHIEN Doctor 小幫手！

-歡迎預約門診

-門診掛號費150元/學生100元
    
-減肥門診/小兒科/家庭醫學科/內科/外科"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg)
    )

################## 顯示封鎖 ####################
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)





if __name__ == '__main__':
    app.run()
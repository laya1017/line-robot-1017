from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('m2UPwMSn3p4xmDvVQkvo+AFGkZONQ0yKm3vQlm/RKMODbcTLoEPhS3oQNsqmWciOl3+hxaSy1LrUGQAJ0AxbaS2yTchTCy7Ux5gsMQmsUYkQSO27KIeDhR78RcekWmeF/zvvuMsmudmHMc0OdukCuQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('aa64bf9da34389763d2020a499d6d6ec')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    res = "你在公三小？"
    if msg in ["道路交通管理處罰條例","道交條例"] :
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=K0040012"))
    elif msg in "波多野結衣" :
        line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url="https://img.ruten.com.tw/s2/e/2e/00/22019535630848_115.jpg",preview_image_url="https://img.ruten.com.tw/s2/e/2e/00/22019535630848_115.jpg"))



if __name__ == "__main__":
    app.run()
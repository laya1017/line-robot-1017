from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
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
    if event.message.text == "girl" :
        image_message = ImageSendMessage(
        original_content_url='https://static.rti.org.tw/assets/thumbnails/2021/04/21/10662432411cdc37527532b8196daf04.jpg',
        preview_image_url='https://static.rti.org.tw/assets/thumbnails/2021/04/21/10662432411cdc37527532b8196daf04.jpg'
        )
        line_bot_api.reply_message(event.reply_token,image_message)
    elif event.message.text in ["hi","Hi","HI","hI"] :
        text_message = TextSendMessage(text='嗨~~~')
        line_bot_api.reply_message(event.reply_token,text_message)
    else :
        text_message = TextSendMessage(text='Plz enter correct text.')
        line_bot_api.reply_message(event.reply_token,text_message)



if __name__ == "__main__":
    app.run()
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackAction,MessageAction,CarouselTemplate,CarouselColumn
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
    if event.message.text in ["新源結衣","新垣結衣","あらがきゆい","Aragaki Yui"] :
        image_message = ImageSendMessage(
        original_content_url='https://static.rti.org.tw/assets/thumbnails/2021/04/21/10662432411cdc37527532b8196daf04.jpg',
        preview_image_url='https://static.rti.org.tw/assets/thumbnails/2021/04/21/10662432411cdc37527532b8196daf04.jpg'
        )
        line_bot_api.reply_message(event.reply_token,image_message)
    elif event.message.text in ["hi","Hi","HI","hI"] :
        text_message = TextSendMessage(text='嗨~~~')
        line_bot_api.reply_message(event.reply_token,text_message)
    else :
        carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title='交通類',
                    text='點選下面按鈕',
                    actions=[
                        PostbackAction(
                            label='法律',
                            display_text='法律',
                        ),
                        PostbackAction(
                            label='常用表格',
                            display_text='常用表格',
                        ),
                        PostbackAction(
                            label='舉發小幫手',
                            display_text='舉發小幫手',
                        )
                    ]
                ),
                CarouselColumn(
                    title='刑事類',
                    text='點選下面按鈕',
                    actions=[
                        PostbackAction(
                            label='法律',
                            display_text='法律',
                        ),
                        PostbackAction(
                            label='常用表格',
                            display_text='常用表格',
                        )
                    ]
                )
            ]
        )
    )
        line_bot_api.reply_message(event.reply_token,carousel_template_message)




if __name__ == "__main__":
    app.run()
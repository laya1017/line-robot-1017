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
                    title='汽機車違規',
                    text='description1',
                    actions=[
                        PostbackAction(
                            label='牌照、駕照違規',
                            display_text='牌照、駕照違規',
                            data='牌照、駕照違規'
                        ),
                        PostbackAction(
                            label='駕駛行為違規',
                            display_text='駕駛行為違規',
                            data='駕駛行為違規'
                        )
                    ]
                ),
                CarouselColumn(
                    title='慢車違規',
                    text='description2',
                    actions=[
                        PostbackAction(
                            label='一般性違規',
                            display_text='一般性違規',
                            data='一般性違規'
                        ),
                        PostbackAction(
                            label='駕駛行為違規',
                            display_text='駕駛行為違規',
                            data='駕駛行為違規'
                        )
                    ]
                )
            ]
        )
)
        line_bot_api.reply_message(event.reply_token,carousel_template_message)




if __name__ == "__main__":
    app.run()
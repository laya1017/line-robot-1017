from flask import Flask, request, abort
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackAction,MessageAction,CarouselTemplate,CarouselColumn
)
import pandas as pd

import json
df = pd.read_csv("data.csv")
df.set_index("Nos",inplace = True)
app = Flask(__name__)

line_bot_api = LineBotApi('m2UPwMSn3p4xmDvVQkvo+AFGkZONQ0yKm3vQlm/RKMODbcTLoEPhS3oQNsqmWciOl3+hxaSy1LrUGQAJ0AxbaS2yTchTCy7Ux5gsMQmsUYkQSO27KIeDhR78RcekWmeF/zvvuMsmudmHMc0OdukCuQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('aa64bf9da34389763d2020a499d6d6ec')
headers = {"Authorization":"Bearer m2UPwMSn3p4xmDvVQkvo+AFGkZONQ0yKm3vQlm/RKMODbcTLoEPhS3oQNsqmWciOl3+hxaSy1LrUGQAJ0AxbaS2yTchTCy7Ux5gsMQmsUYkQSO27KIeDhR78RcekWmeF/zvvuMsmudmHMc0OdukCuQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

# body = {
#           "size": {"width": 2500, "height": 843},
#           "selected": True,
#           "name": "圖文選單 1",
#           "chatBarText": "查看更多資訊",
#           "areas": [
#             {
#               "bounds": {"x": 0, "y": 0, "width": 842, "height": 839},
#               "action": {"type": "message", "text": "[[怎麼查詢法條]]"}
#             },
#             {
#               "bounds": {"x": 847, "y": 8, "width": 802, "height": 835},
#               "action": {"type": "message","text": "[[酒(毒)駕專區]]"}
#             },
#             {
#               "bounds": {"x": 1653, "y": 9, "width": 847, "height": 834},
#               "action": {"type": "message","text": "[[交通常見問題]]"}
#             }
#           ]
#         }
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',headers=headers,data=json.dumps(body).encode('utf-8'))
# print(req.text)


rich_menu_id = 'richmenu-47a80981c4a0f73c5f857317ee081b0b'

# with open("rich_menu.png", 'rb') as f:
#     line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
                       headers=headers)
print(req.text)
rich_menu_list = line_bot_api.get_rich_menu_list()
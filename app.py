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
df = pd.read_csv("data.csv")
df.set_index("Nos",inplace = True)
sort = list(df.index)
# use DateTime
import datetime
import search
#all carousel templates
def Other_QnA():
    QA = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=[
            CarouselColumn(
                title='處罰機關如何判斷？',
                text='以戶籍地還是駕籍地舉發呢？',
                actions=[
                    MessageAction(
                        label='按我',
                        text='#處罰機關如何判斷？'
                        )
                ]
                ),
            CarouselColumn(
                title='哪些違規不得郵繳？',
                text='至應到案處所裁決還是能直接郵局繳款？',
                actions=[
                    MessageAction(
                        label='按我',
                        text='#哪些違規不得郵繳？'
                        )
                ]
                ),
            CarouselColumn(
                title='當場舉發的應到案日期計算？',
                text='常常算錯QQ',
                actions=[
                    MessageAction(
                        label='按我',
                        text='#當場舉發的應到案日期計算？'
                        )
                    ]
                )
                ]
            )
        )
    return QA
#all carousel templates
#all buttom templates
def searchTutorial():
    st = TemplateSendMessage(alt_text='如何查詢法條？',
    template=ButtonsTemplate(
        title='如何查詢法條？',
        text='目前有：依"條號"查詢以及"關鍵字"查詢。',
        actions=[
            MessageAction(
                label='依條號查詢教學',
                text='searchByArticles'
                ),
            MessageAction(
                label='依關鍵字查詢教學',
                text='searchByKeywords'
                )
        ]
    )
    )
    return st
def dateTimeCaculator():
    st = TemplateSendMessage(alt_text='應到案日期計算',
    template=ButtonsTemplate(
        title='應到案日期計算',
        text='目前僅開放今日的當場舉發應到案日期計算',
        actions=[
            MessageAction(
                label='現場舉發應到案日期',
                text="現場舉發應到案日期(今天)"
                )
        ]
    )
    )
    return st
#all buttom templates
app = Flask(__name__)
line_bot_api = LineBotApi('m2UPwMSn3p4xmDvVQkvo+AFGkZONQ0yKm3vQlm/RKMODbcTLoEPhS3oQNsqmWciOl3+hxaSy1LrUGQAJ0AxbaS2yTchTCy7Ux5gsMQmsUYkQSO27KIeDhR78RcekWmeF/zvvuMsmudmHMc0OdukCuQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('aa64bf9da34389763d2020a499d6d6ec')
headers = {"Authorization":"Bearer m2UPwMSn3p4xmDvVQkvo+AFGkZONQ0yKm3vQlm/RKMODbcTLoEPhS3oQNsqmWciOl3+hxaSy1LrUGQAJ0AxbaS2yTchTCy7Ux5gsMQmsUYkQSO27KIeDhR78RcekWmeF/zvvuMsmudmHMc0OdukCuQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

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
    if msg in ["新源結衣","新垣結衣","あらがきゆい","Aragaki Yui"] :
        image_message = ImageSendMessage(
        original_content_url='https://static.rti.org.tw/assets/thumbnails/2021/04/21/10662432411cdc37527532b8196daf04.jpg',
        preview_image_url='https://static.rti.org.tw/assets/thumbnails/2021/04/21/10662432411cdc37527532b8196daf04.jpg'
        )
        line_bot_api.reply_message(event.reply_token,image_message)
    elif msg in ["hi","Hi","HI","hI"] :
        text_message = TextSendMessage(text='嗨~~~')
        line_bot_api.reply_message(event.reply_token,text_message)
    elif msg == "[[怎麼查詢法條]]" :
        line_bot_api.reply_message(event.reply_token,searchTutorial())
    elif msg == "searchByArticles" :
        text_message = TextSendMessage(text="以條號搜尋：\n先打$記號，然後接續打上阿拉伯數字條號，格式為$條,項,款。例如：$48 即可得到48條所有內容；輸入$48,1，即可得到48條1項所有條款；輸入$48,1,2，即可得到48條1項2款(有的法條只有條及款，例如49條2款，應輸入$49,,2即可得到該內容。")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif msg == "searchByKeywords" :
        text_message = TextSendMessage(text="以關鍵字搜尋：\n按左下角類似鍵盤的按鈕，然後在對話發送欄區打@記號，然後在@後方打上關鍵字，例如：@闖紅燈。\n也可使用多條件查詢，例如：@執照 未領(中間用空白區隔)。")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif "@" in msg : # Use Content_finder function to find laws
        msg = msg.replace("@","")
        if "迴轉" in msg or "雙黃" in msg or "雙黃線" in msg : 
            msg = msg.replace("迴轉","")
            msg = msg.replace("雙黃線","雙黃")
            msg = msg.replace("雙黃","分向限制線、禁止超車線")
            result = search.NosFiltWords("33,1,7",msg) + search.NosFiltWords("49",msg) + search.NosFiltWords("54,,3",msg).strip("\n")
            text_message = TextSendMessage(text=result)
        elif "兩段式" in msg or "兩段" in msg :
            if "慢車" in msg :
                result  =search.getByNos("73,1,3").strip("\n")
                text_message = TextSendMessage(text=result)
            else:
                result = search.getByNos("48,1,2") + search.getByNos("73,1,3").strip("\n")
                text_message = TextSendMessage(text=result)
        elif "逆向" in msg or "停車" in msg or "臨停" in msg or "違停" in msg or "行駛" in msg:
            msg = msg.replace("臨停","臨時停車")
            msg = msg.replace("違停","停車")
            if ("停車" in msg or "臨時停車" in msg) and "逆向" in msg :
                msg += "順行"
            msg = msg.replace("逆向","")
            result = search.NosFiltWords("45,1,1",msg)+"\n" + search.NosFiltWords("45,1,3",msg)+"\n" +search.NosFiltWords("55",msg)+"\n" + search.NosFiltWords("56",msg)+"\n" + search.NosFiltWords("74,1,2",msg)
            text_message = TextSendMessage(text=result.strip("\n"))
        elif "紅" in msg:
            if "右" in msg:
                if "慢" in msg:
                    result = search.getByNos("74,1,1").strip("\n")
                    text_message = TextSendMessage(text=result)
                elif "汽車" in msg or "機車" in msg:
                    result = search.getByNos("53,2").strip("\n")
                    text_message = TextSendMessage(text=result)
                elif "大眾" in msg:
                    result = search.getByNos("53-1,2").strip("\n")
                    text_message = TextSendMessage(text=result)
                else :
                    result = search.getByNos("53,2") + search.getByNos("53-1,2") + search.getByNos("74,1,1").strip("\n")
                    text_message = TextSendMessage(text=result)
            elif "闖" in msg:
                if "慢" in msg:
                    result = search.getByNos("74,1,1").strip("\n")
                    text_message = TextSendMessage(text=result)
                elif "汽車" in msg or "機車" in msg:
                    result = search.getByNos("53,1").strip("\n")
                    text_message = TextSendMessage(text=result)
                elif "大眾" in msg:
                    result = search.getByNos("53-1,1").strip("\n")
                    text_message = TextSendMessage(text=result)
                else :                    
                    result = search.getByNos("53,1") + search.getByNos("53-1,1") + search.getByNos("74,1,1").strip("\n")
                    text_message = TextSendMessage(text=result)
            elif "慢" in msg:
                result = search.getByNos("74,1,1").strip("\n")
                text_message = TextSendMessage(text=result)
            elif "汽車" in msg or "機車" in msg:
                result = search.getByNos("53").strip("\n")
                text_message = TextSendMessage(text=result)
            else :
                result = search.getByNos("53") + search.getByNos("53-1") + search.getByNos("74,1,1").strip("\n")
                text_message = TextSendMessage(text=result)
        elif "方向燈" in msg or "大燈" in msg or "霧燈" in msg :
            result = search.getByNos("42").strip("\n")
            text_message = TextSendMessage(text=result)
        elif "危險駕駛" in msg or "危駕" in msg or "危險駕車" in msg or "超速" in msg :
            if "超速" in msg :
                msg = msg.replace("超速","最高時速")
                result = search.NosFiltWords("40",msg) + search.NosFiltWords("43,1",msg)
            else :
                msg = msg.replace("危險駕駛","")
                msg = msg.replace("危駕","")
                msg = msg.replace("危險駕車","")
                result = search.NosFiltWords("43",msg)
            text_message = TextSendMessage(text=result.strip("\n"))
        elif "酒駕" in msg or "酒" in msg or "毒駕" in msg or "毒" in msg or "拒測" in msg or "累犯" in msg or "累" in msg :
            msg = msg.replace("累犯","累")
            msg = msg.replace("累","十年")
            if "拒測" in msg :
                msg = msg.replace("拒測","")
                msg = msg.replace("酒駕","酒")
                msg = msg.replace("酒","")
                msg = msg.replace("毒駕","毒")
                msg = msg.replace("毒","")
                msg = msg.replace("拒測","")
                result = search.NosFiltWords("35,4",msg) + search.NosFiltWords("35,5",msg) + search.NosFiltWords("73,3",msg)
            elif "酒駕" in msg or "酒" in msg:
                msg = msg.replace("酒駕","酒")
                msg = msg.replace("酒","")
                result = search.NosFiltWords("35,1",msg) + search.NosFiltWords("35,3",msg) + search.NosFiltWords("35,7",msg) + search.NosFiltWords("35,8",msg) + search.NosFiltWords("74,2",msg)
            elif "毒駕" in msg or "毒" in msg:
                msg = msg.replace("毒駕","毒")
                msg = msg.replace("毒","")
                result = search.NosFiltWords("35,1",msg + " 藥") + search.NosFiltWords("35,3",msg) + search.NosFiltWords("35,7",msg)
            text_message = TextSendMessage(text=result)
        else:
            result = search.Content_finder(msg)
            text_message = TextSendMessage(text=result)
        line_bot_api.reply_message(event.reply_token,text_message)
    elif "$" in msg : # Use number function to find laws
        words = msg.replace("$","")
        search.getByNos(words)
        text_message = TextSendMessage(text=search.getByNos(words))
        line_bot_api.reply_message(event.reply_token,text_message)
    elif msg == "[[酒(毒)駕專區]]" :
        text_message = TextSendMessage(text="Sorry 還沒開放喔!")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif msg == "[[交通常見問題]]" : 
        line_bot_api.reply_message(event.reply_token,Other_QnA())
    elif msg == "#處罰機關如何判斷？" :
        text_message = TextSendMessage(text="依據違反道路交通管理事件統一裁罰基準及處理細則第25條規定：\n舉發汽車違反道路交通管理事件，以汽車所有人為處罰對象者，移送其車籍地處罰機關處理；以駕駛人或乘客為處罰對象者，移送其駕籍地處罰機關處理；駕駛人或乘客未領有駕駛執照者，移送其戶籍地處罰機關處理。但有下列情形之一者，移送行為地處罰機關處理：\n一、汽車肇事致人傷亡。\n二、抗拒稽查致傷害。\n三、汽車駕駛人或乘客未領有駕駛執照且無法查明其戶籍所在地。\n四、汽車買賣業或汽車修理業違反本條例第五十七條規定。\n五、汽車駕駛人違反本條例第三十五條規定。\n計程車駕駛人有本條例第三十六條或第三十七條之情形，應受吊扣執業登記證或廢止執業登記處分者，移送其辦理執業登記之警察機關處理。\n以大眾捷運系統營運機構為被通知人舉發違反道路交通管理事件者，移送其營運機構監督機關所在地處罰機關處理。")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif msg == "#哪些違規不得郵繳？" :
        text_message = TextSendMessage(text="依交通部108.07.16.交路字第1080021339號函，不得郵繳的有：\n第十二條\n第十三條\n第十五條第一項第二款、第五款\n第十六條第一項第五款\n第十七條\n第十八條\n第十八條之一\n第二十條\n第二十一條\n第二十一條之一\n第二十三條\n第二十四條\n第二十六條\n第二十七條第二項\n第二十九條第四項\n第二十九條之二第三項、第五項\n第三十條第三項\n第三十一條第四項\n第三十四條後段\n第三十五條第一項至第五項、第七項\n第三十六條第二項、第三項\n第三十七條\n第四十三條\n第四十五條第二項、第三項\n第五十四條\n第六十條第一項\n第六十一條\n第六十二條第一項、第四項及第五項")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif msg == "#當場舉發的應到案日期計算？" :
        line_bot_api.reply_message(event.reply_token,dateTimeCaculator())
    elif msg == "現場舉發應到案日期(今天)":
        today = datetime.datetime.now()
        initialdate = str(today.year - 1911) + '-' + str(today.month) + '-' + str(today.day)
        expiryDate = today + datetime.timedelta(days = 30)
        finalDate = str(expiryDate.year - 1911) + '-' + str(expiryDate.month) + '-' + str(expiryDate.day)
        text_message = TextSendMessage(text="今天日期為：\n"+initialdate + "\n應到案日期為：\n" + finalDate)
        line_bot_api.reply_message(event.reply_token,text_message)
    elif msg in ["打炮","機掰","幹你娘","丁福氣","幹"] :
        text_message = TextSendMessage(text="不要輸入那些屋ㄟ某欸啦....")
        line_bot_api.reply_message(event.reply_token,text_message)
    else :
        text_message = TextSendMessage(text="哈囉，請點開左下角可看見選單才知道如何使用～")
        line_bot_api.reply_message(event.reply_token,text_message)
if __name__ == "__main__":
    app.run()
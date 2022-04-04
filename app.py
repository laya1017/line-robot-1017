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
today = datetime.datetime.now()

initialdate = str(today.year - 1911) + '-' + str(today.month) + '-' + str(today.day)
expiryDate = today + datetime.timedelta(days = 30)
finalDate = str(expiryDate.year - 1911) + '-' + str(expiryDate.month) + '-' + str(expiryDate.day)
# Use number find laws
def getText(_list):
    df = pd.read_csv("data.csv")
    df.set_index("Nos",inplace = True)
    result_df = df.loc[_list]
    result_text = []
    for i in range(0,len(result_df)):
        result_text.append(result_df.index[i] + "：\n" + result_df["Contents"][i] + "\n處罰：" + result_df["Punishment"][i] + "\n註記：\n" + result_df["Remark"][i].strip("\n") + "\n")
    return "".join(result_text)
def listByArticle(A = ""):
    df = pd.read_csv("data.csv")
    df.set_index("Nos",inplace = True)
    index_list = []
    unique = []
    for i in df.index :
        if (len(str(A) + "條") == len(i[:i.index("條") + 1])) and (str(A) + "條" == i[:i.index("條") + 1]):
            index_list.append(i)
    for i in index_list:
        if i not in unique:
            unique.append(i)
    return unique
def listByPara(P = ""):
    df = pd.read_csv("data.csv")
    df.set_index("Nos",inplace = True)
    index_list = []
    unique = []
    for i in df.index :
        if "項" in i:
            if (len(str(P) + "項") == len(i[i.index("條") + 1:i.index("項") + 1])) and (str(P) + "項" == i[i.index("條") + 1:i.index("項") + 1]):
                index_list.append(i)
        else:
            continue
    for i in index_list:
        if i not in unique:
            unique.append(i)
    return unique
def listBySub(S = ""):
    df = pd.read_csv("data.csv")
    df.set_index("Nos",inplace = True)
    index_list = []
    unique = []
    for i in df.index :
        if "款" in i and "項" in i:
            if (len(str(S) + "款") == len(i[i.index("項") + 1:i.index("款") + 1])) and (str(S) + "款" == i[i.index("項") + 1:i.index("款") + 1]):
                index_list.append(i)
        elif "款" in i and "項" not in i:
            if (len(str(S) + "款") == len(i[i.index("條") + 1:i.index("款") + 1])) and (str(S) + "款" == i[i.index("條") + 1:i.index("款") + 1]):
                index_list.append(i)
    for i in index_list:
        if i not in unique:
            unique.append(i)
    return unique
def getByNos(words):
    keys = words.split(",")
    a = keys[0]
    try:
        p = keys[1]
    except IndexError:
        p = ""
    try:
        s = keys[2]
    except IndexError:
        s = "" 
    A = listByArticle(a)
    P = listByPara(p)
    S = listBySub(s)
    result = list(set(A) & set(P) & set(S))
    if result == [] :
        if set(A) & set(P) != set(): # 先判斷有沒有項
            result = set(A) & set(P)
            if result & set(S) != set():
                result = list(result & set(S))
            else:
                result = list(set(A) & set(P))
        elif set(A) & set(P) == set():
            result = set(A)
            if result & set(S) != set():
                result = list(result & set(S))
            else:
                result = list(set(A))
        else:
            result = list(set(A))
    result.sort(key = sort.index)
    return getText(result)
# Use number find laws

# Use keywords find laws
def Content_finder(words):
    temp = df
    keys = words.split(" ")
    for key in keys :
        condition = temp["Contents"].str.contains(key)
        temp = temp[condition]
    result = []
    for i in range(0,len(temp)):
        result.append(temp.index[i] + "：\n" + temp['Contents'][i] +
             "\n處罰：" + temp["Punishment"][i].strip("\n") + "\n註記：\n" + temp["Remark"][i] + "\n")
    return "".join(result).strip("\n")
# Use keywords find laws


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
    if event.message.text in ["新源結衣","新垣結衣","あらがきゆい","Aragaki Yui"] :
        image_message = ImageSendMessage(
        original_content_url='https://static.rti.org.tw/assets/thumbnails/2021/04/21/10662432411cdc37527532b8196daf04.jpg',
        preview_image_url='https://static.rti.org.tw/assets/thumbnails/2021/04/21/10662432411cdc37527532b8196daf04.jpg'
        )
        line_bot_api.reply_message(event.reply_token,image_message)
    elif event.message.text in ["hi","Hi","HI","hI"] :
        text_message = TextSendMessage(text='嗨~~~')
        line_bot_api.reply_message(event.reply_token,text_message)
    elif event.message.text == "[[怎麼查詢法條]]" :
        line_bot_api.reply_message(event.reply_token,searchTutorial())
    elif event.message.text == "searchByArticles" :
        text_message = TextSendMessage(text="以條號搜尋：\n先打$記號，然後接續打上阿拉伯數字條號，格式為$條,項,款。例如：$48 即可得到48條所有內容；輸入$48,1，即可得到48條1項所有條款；輸入$48,1,2，即可得到48條1項2款(有的法條只有條及款，例如49條2款，應輸入$49,,2即可得到該內容。")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif event.message.text == "searchByKeywords" :
        text_message = TextSendMessage(text="以關鍵字搜尋：\n按左下角類似鍵盤的按鈕，然後在對話發送欄區打@記號，然後在@後方打上關鍵字，例如：@闖紅燈。\n也可使用多條件查詢，例如：@執照 未領(中間用空白區隔)。")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif "@" in event.message.text : # Use Content_finder function to find laws
        if "迴轉" in event.message.text: 
            event.message.text = (event.message.text).replace("迴轉"," 迴車")
        elif "雙黃線" in event.message.text:
            event.message.text = (event.message.text).replace("雙黃線"," 分向限制線")
        elif "兩段式" in event.message.text:
            event.message.text = (event.message.text).replace("兩段式"," 轉彎 不依標誌 標線 號誌指示")
        # if "酒駕" in event.message.text:
        #     (event.message.text).replace("酒駕","酒精")
        # if "拒測" in event.message.text:
        #     (event.message.text).replace("拒測","酒精")
        result = Content_finder((event.message.text).replace("@",""))
        text_message = TextSendMessage(text=Content_finder((event.message.text).replace("@","")))
        line_bot_api.reply_message(event.reply_token,text_message)
    elif "$" in event.message.text : # Use number function to find laws
        words = (event.message.text).replace("$","")
        getByNos(words)
        text_message = TextSendMessage(text=getByNos(words))
        line_bot_api.reply_message(event.reply_token,text_message)
    elif event.message.text == "[[酒(毒)駕專區]]" :
        text_message = TextSendMessage(text="Sorry 還沒開放喔!")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif event.message.text == "[[交通常見問題]]" : 
        line_bot_api.reply_message(event.reply_token,Other_QnA())
    elif event.message.text == "#處罰機關如何判斷？" :
        text_message = TextSendMessage(text="依據違反道路交通管理事件統一裁罰基準及處理細則第25條規定：\n舉發汽車違反道路交通管理事件，以汽車所有人為處罰對象者，移送其車籍地處罰機關處理；以駕駛人或乘客為處罰對象者，移送其駕籍地處罰機關處理；駕駛人或乘客未領有駕駛執照者，移送其戶籍地處罰機關處理。但有下列情形之一者，移送行為地處罰機關處理：\n一、汽車肇事致人傷亡。\n二、抗拒稽查致傷害。\n三、汽車駕駛人或乘客未領有駕駛執照且無法查明其戶籍所在地。\n四、汽車買賣業或汽車修理業違反本條例第五十七條規定。\n五、汽車駕駛人違反本條例第三十五條規定。\n計程車駕駛人有本條例第三十六條或第三十七條之情形，應受吊扣執業登記證或廢止執業登記處分者，移送其辦理執業登記之警察機關處理。\n以大眾捷運系統營運機構為被通知人舉發違反道路交通管理事件者，移送其營運機構監督機關所在地處罰機關處理。")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif event.message.text == "#哪些違規不得郵繳？" :
        text_message = TextSendMessage(text="依交通部108.07.16.交路字第1080021339號函，不得郵繳的有：\n第十二條\n第十三條\n第十五條第一項第二款、第五款\n第十六條第一項第五款\n第十七條\n第十八條\n第十八條之一\n第二十條\n第二十一條\n第二十一條之一\n第二十三條\n第二十四條\n第二十六條\n第二十七條第二項\n第二十九條第四項\n第二十九條之二第三項、第五項\n第三十條第三項\n第三十一條第四項\n第三十四條後段\n第三十五條第一項至第五項、第七項\n第三十六條第二項、第三項\n第三十七條\n第四十三條\n第四十五條第二項、第三項\n第五十四條\n第六十條第一項\n第六十一條\n第六十二條第一項、第四項及第五項")
        line_bot_api.reply_message(event.reply_token,text_message)
    elif event.message.text == "#當場舉發的應到案日期計算？" :
        line_bot_api.reply_message(event.reply_token,dateTimeCaculator())
    elif event.message.text == "現場舉發應到案日期(今天)":
        today = datetime.datetime.now()
        initialdate = str(today.year - 1911) + '-' + str(today.month) + '-' + str(today.day)
        expiryDate = today + datetime.timedelta(days = 30)
        finalDate = str(expiryDate.year - 1911) + '-' + str(expiryDate.month) + '-' + str(expiryDate.day)
        text_message = TextSendMessage(text="今天日期為：\n"+initialdate + "\n應到案日期為：\n" + finalDate)
        line_bot_api.reply_message(event.reply_token,text_message)
    elif event.message.text in ["打炮","機掰","幹你娘","丁福氣","幹"] :
        text_message = TextSendMessage(text="不要輸入那些屋ㄟ某欸啦....")
        line_bot_api.reply_message(event.reply_token,text_message)
    else :
        text_message = TextSendMessage(text="哈囉，請點開左下角可看見選單才知道如何使用～")
        line_bot_api.reply_message(event.reply_token,text_message)
if __name__ == "__main__":
    app.run()
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, render_template
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackAction,MessageAction,CarouselTemplate,CarouselColumn,QuickReply,QuickReplyButton
)
import datetime
import search
import pandas as pd
df = pd.read_csv("data.csv")
df.set_index("Nos",inplace = True)
sort = list(df.index)
app = Flask(__name__)
##Columns
def enter_nos_mode(event):
    reply = TemplateSendMessage(alt_text="條號搜尋模式。\n請輸入條號(第＿條)：",
        template=ButtonsTemplate(
            title="條號搜尋模式。\n請輸入條號：",
            text='若要繼續查詢則直接輸入',
            actions=[
                MessageAction(
                    label="離開",
                    text="Exit"
                    )
            ]
        ))
    return reply
def enter_txt_mode(event):
    reply = TemplateSendMessage(
        alt_text="關鍵字搜尋模式。\n請輸入關鍵字：",
        quick_reply=QuickReply(
            items=[
            QuickReplyButton(action=MessageAction(label="無照", text="無照")),
            QuickReplyButton(action=MessageAction(label="駕照 吊銷", text="駕照 吊銷")),
            QuickReplyButton(action=MessageAction(label="牌照 吊扣", text="牌照 吊扣")),
            QuickReplyButton(action=MessageAction(label="牌照 吊扣", text="牌照 吊銷")),
            QuickReplyButton(action=MessageAction(label="牌照 吊銷", text="牌照 吊銷")),
            QuickReplyButton(action=MessageAction(label="拼裝車", text="拼裝車")),
            QuickReplyButton(action=MessageAction(label="逆向 行駛(可以改為停車)", text="逆向 行駛")),
            QuickReplyButton(action=MessageAction(label="兩段式", text="兩段式")),
            QuickReplyButton(action=MessageAction(label="紅燈", text="紅燈")),
            QuickReplyButton(action=MessageAction(label="危險駕車", text="危險駕車")),
            QuickReplyButton(action=MessageAction(label="肇事 逃逸 受傷", text="肇事 逃逸 受傷")),
            QuickReplyButton(action=MessageAction(label="肇事 逃逸 無 傷", text="肇事 逃逸 無 傷")),
            QuickReplyButton(action=MessageAction(label="不服稽查 逃逸", text="不服稽查 逃逸"))]),
        template=ButtonsTemplate(
            title="關鍵字搜尋模式。\n請輸入關鍵字：",
            text='1.若要繼續查詢則直接輸入\n2.空白區隔關鍵字可使用多條件查詢\n3.下方按鈕為範例',
            actions=[
                MessageAction(
                    label="離開",
                    text="Exit"
                    )
            ]
        ))
    return reply
def Other_QnA(event):
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
                        text='處罰機關如何判斷？'
                        )
                ]
                ),
            CarouselColumn(
                title='哪些違規不得郵繳？',
                text='至應到案處所裁決還是能直接郵局繳款？',
                actions=[
                    MessageAction(
                        label='按我',
                        text='哪些違規不得郵繳？'
                        )
                ]
                )
                ]
            )
        )
    return QA
def selects_nos_mode_P(event,uid,Nos):
    reply = TemplateSendMessage(alt_text="第"+ Nos + "條第＿項？",
        template=ButtonsTemplate(
            title="第"+ Nos + "條第＿項？",
            text='若要繼續查詢則直接輸入',
            actions=[
                MessageAction(
                    label="列出第"+Nos+"條的所有法條",
                    text="列出第"+Nos+"條的所有法條"
                    ),
                MessageAction(
                    label='上一步',
                    text='Previous-nos_mode'
                    ),
                MessageAction(
                    label='離開',
                    text='Exit'
                    )
            ]
        ))
    return reply
def selects_nos_mode_S(event,uid,Nos):
    reply = TemplateSendMessage(alt_text="第"+ Nos + "條第＿款？",
        template=ButtonsTemplate(
            title="第"+ Nos + "條第＿款？",
            text='若要繼續查詢則直接輸入',
            actions=[
                MessageAction(
                    label="列出第"+Nos+"條的所有法條",
                    text="列出第"+Nos+"條的所有法條"
                    ),
                MessageAction(
                    label='上一步',
                    text='Previous-nos_mode'
                    ),
                MessageAction(
                    label='離開',
                    text='Exit'
                    )
            ]
        ))
    return reply
def selects_nos_mode_P_S(event,uid,Nos,NosP):
    reply = TemplateSendMessage(alt_text="第"+ Nos + "條第"+NosP + "項第＿款？",
        template=ButtonsTemplate(
            title="第"+ Nos + "條第"+NosP + "項第＿款？",
            text='若要繼續查詢則直接輸入',
            actions=[
                MessageAction(
                    label="第"+ Nos + "條第"+NosP+"項的所有法條",
                    text="第"+ Nos + "條第"+NosP+"項的所有法條"
                    ),
                MessageAction(
                    label='上一步',
                    text='Previous-nos_mode_P'
                    ),
                MessageAction(
                    label='離開',
                    text='Exit'
                    )
            ]
        ))
    return reply
##Columns

##dwiNdwd zone
def dwiNdwdbuttonFilt(msg):
    quick_reply=QuickReply(
        items=[
        QuickReplyButton(action=MessageAction(label="汽機車酒駕法條", text="汽機車酒駕法條")),
        QuickReplyButton(action=MessageAction(label="汽機車毒駕法條", text="汽機車毒駕法條")),
        QuickReplyButton(action=MessageAction(label="累犯法條", text="累犯法條")),
        QuickReplyButton(action=MessageAction(label="汽機車酒駕拒測法條", text="汽機車酒駕拒測法條")),
        QuickReplyButton(action=MessageAction(label="拒測累犯法條", text="拒測累犯法條")),
        QuickReplyButton(action=MessageAction(label="汽機車酒駕拒測告知", text="汽機車酒駕拒測告知")),
        QuickReplyButton(action=MessageAction(label="慢車酒駕法條", text="慢車酒駕法條")),
        QuickReplyButton(action=MessageAction(label="慢車酒駕拒測法條", text="慢車酒駕拒測法條")),
        QuickReplyButton(action=MessageAction(label="回到酒(毒)駕區", text="回到酒(毒)駕區")),
        ]
        )
    for i in quick_reply.items:
        if msg == i.action.label:
            quick_reply.items.remove(i)
    return quick_reply
def dwiNdwdenterButtons(event,msg):
    reply = TemplateSendMessage(alt_text="酒(毒)駕專區",
        quick_reply=dwiNdwdbuttonFilt(msg),
        template=ButtonsTemplate(
            title="酒(毒)駕專區",
            text='請點選下面按鈕',
            actions=[
                MessageAction(
                    label="取締酒(毒)駕規定",
                    text="DWI and DUD"
                    ),
                MessageAction(
                    label='員警告發須知(最新修訂)',
                    text='The Newist Announcement'
                    ),
                MessageAction(
                    label='離開',
                    text='Exit'
                    )
            ]
        ))
    return reply
def dwiNdwd(event):
    reply = TemplateSendMessage(alt_text="酒(毒)駕專區",
        template=ButtonsTemplate(
            title="酒駕與毒駕",
            text='最下排為快速鈕',
            actions=[
                MessageAction(
                    label="取締「酒」駕規定",
                    text="DWI Regulation"
                    ),
                MessageAction(
                    label="取締「毒」駕規定",
                    text='DWD Regulation'
                    ),
                MessageAction(
                    label="上一步",
                    text="Back to dwiNdwdenterButtons"
                    ),
                MessageAction(
                    label="離開",
                    text='Exit'
                    )
            ]
        ))
    return reply
def dwimode(event):
    reply = TemplateSendMessage(alt_text="「酒」駕規定區",
        template=ButtonsTemplate(
            title="「酒」駕規定區",
            text='點選處罰車種',
            actions=[
                MessageAction(
                    label="汽機車",
                    text="Cars and Scooters"
                    ),
                MessageAction(
                    label="慢車",
                    text='Slow-moving vehicles'
                    ),
                MessageAction(
                    label="上一步",
                    text="Back to dwiNdwd"
                    ),
                MessageAction(
                    label="離開",
                    text='Exit'
                    )
            ]
        ))
    return reply
def dwimode_CNS(event):
    reply = TemplateSendMessage(alt_text="汽機車酒駕違規態樣",
        template=ButtonsTemplate(
            title="汽機車酒駕違規態樣",
            text='點選違規態樣',
            actions=[
                MessageAction(
                    label="超標舉發",
                    text="Exceed The Maximum Tolerate Standard"
                    ),
                MessageAction(
                    label="拒測舉發",
                    text='Refuses To Take The Test'
                    ),
                MessageAction(
                    label="上一步",
                    text="Back to dwimode"
                    ),
                MessageAction(
                    label="離開",
                    text='Exit'
                    )
            ]
        ))
    return reply
def dwimode_CNS_Ex(event):
    reply = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=[
            CarouselColumn(
                title='駕駛人(酒駕超標)',
                text='初犯與累犯',
                actions=[
                    MessageAction(
                        label='初犯',
                        text='First Violation'
                        ),
                    MessageAction(
                        label='十年內累犯兩次或三次',
                        text='Recidivism'
                        ),
                    MessageAction(
                        label='應注意事項',
                        text='Dos and Don\'ts'
                        )
                ]
                ),
            CarouselColumn(
                title='所有人與同車乘客處罰(酒駕超標)',
                text=' ',
                actions=[
                    MessageAction(
                        label='所有人處罰',
                        text='Owner'
                        ),
                    MessageAction(
                        label='同車乘客處罰',
                        text='Passenger'
                        ),
                    MessageAction(
                        label='免罰要件',
                        text='Impunity Condition'
                        )

                ]
                ),
            CarouselColumn(
                title='其他',
                text=' ',
                actions=[
                    MessageAction(
                        label='轉換至拒測規定',
                        text='Lead To dwimode_CNS_Re'
                        ),
                    MessageAction(
                        label='上一步',
                        text='Back to dwimode_CNS'
                        ),
                    MessageAction(
                        label='離開',
                        text='Exit'
                        )

                ]
                )
                ]
            )
        )
    return reply
def dwimode_CNS_Re(event):
    reply = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=[
            CarouselColumn(
                title='駕駛人(酒駕拒測)',
                text='初犯與累犯',
                actions=[
                    MessageAction(
                        label='初犯',
                        text='First Violation'
                        ),
                    MessageAction(
                        label='十年內累犯兩次或三次',
                        text='Recidivism'
                        ),
                    MessageAction(
                        label='應告知事項',
                        text='Notification'
                        )
                ]
                ),
            CarouselColumn(
                title='其他',
                text='轉換模式、上一步、離開',
                actions=[
                    MessageAction(
                        label='轉換至酒測規定',
                        text='Lead To dwimode_CNS_Ex'
                        ),
                    MessageAction(
                        label='上一步',
                        text='Back to dwimode_CNS'
                        ),
                    MessageAction(
                        label='離開',
                        text='Exit'
                        )

                ]
                )
                ]
            )
        )
    return reply
def dwdmode(event):
    reply = TemplateSendMessage(alt_text="「毒」駕規定區",
        template=ButtonsTemplate(
            title="「毒」駕規定區",
            text='點選處罰車種',
            actions=[
                MessageAction(
                    label="汽機車",
                    text="Cars and Scooters"
                    ),
                MessageAction(
                    label="慢車",
                    text='SMV No DWD'
                    ),
                MessageAction(
                    label="上一步",
                    text="Back to dwiNdwd"
                    ),
                MessageAction(
                    label="離開",
                    text='Exit'
                    )
            ]
        ))
    return reply
def dwdmode_CNS(event):
    reply = TemplateSendMessage(alt_text="汽機車毒駕違規態樣",
        template=ButtonsTemplate(
            title="汽機車毒駕違規態樣",
            text='點選違規態樣',
            actions=[
                MessageAction(
                    label="毒駕舉發",
                    text="Exceed The Maximum Tolerate Standard"
                    ),
                MessageAction(
                    label="拒測舉發",
                    text='Refuses To Take The Test'
                    ),
                MessageAction(
                    label="上一步",
                    text="Back to dwdmode"
                    ),
                MessageAction(
                    label="離開",
                    text='Exit'
                    )
            ]
        ))
    return reply
def dwdmode_CNS_Ex(event):
    reply = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=[
            CarouselColumn(
                title='駕駛人(毒駕舉發)',
                text='初犯與累犯',
                actions=[
                    MessageAction(
                        label='初犯',
                        text='First Violation'
                        ),
                    MessageAction(
                        label='十年內累犯兩次或三次',
                        text='Recidivism'
                        ),
                    MessageAction(
                        label='應注意事項',
                        text='Dos and Don\'ts'
                        )
                ]
                ),
            CarouselColumn(
                title='所有人與同車乘客處罰(毒駕舉發)',
                text=' ',
                actions=[
                    MessageAction(
                        label='所有人處罰',
                        text='Owner'
                        ),
                    MessageAction(
                        label='同車乘客處罰(沒有毒駕處罰)',
                        text='Passenger'
                        ),
                    MessageAction(
                        label='免罰要件',
                        text='Impunity Condition'
                        )

                ]
                ),
            CarouselColumn(
                title='其他',
                text=' ',
                actions=[
                    MessageAction(
                        label='轉換至拒測規定',
                        text='Lead To dwdmode_CNS_Re'
                        ),
                    MessageAction(
                        label='上一步',
                        text='Back to dwdmode_CNS'
                        ),
                    MessageAction(
                        label='離開',
                        text='Exit'
                        )

                ]
                )
                ]
            )
        )
    return reply
def dwdmode_CNS_Re(event):
    reply = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=[
            CarouselColumn(
                title='駕駛人(毒駕拒測)',
                text='初犯與累犯',
                actions=[
                    MessageAction(
                        label='初犯',
                        text='First Violation'
                        ),
                    MessageAction(
                        label='十年內累犯兩次或三次',
                        text='Recidivism'
                        ),
                    MessageAction(
                        label='應告知事項',
                        text='Notification'
                        )
                ]
                ),
            CarouselColumn(
                title='回上一步或離開',
                text=' ',
                actions=[
                    MessageAction(
                        label='轉換至毒駕舉發規定',
                        text='Lead to dwdmode_CNS_Ex'
                        ),
                    MessageAction(
                        label='上一步',
                        text='Back to dwdmode_CNS'
                        ),
                    MessageAction(
                        label='離開',
                        text='Exit'
                        )

                ]
                )
                ]
            )
        )
    return reply
def dwdmode_SMV(event):
    reply = TextSendMessage(
        text = """一、慢車於道路交通管理處罰條例第73條2項及3項皆處罰為「\"酒精\"濃度超標」及「拒絕\"酒精\"濃度測試」，且於同法中並\"無\"規定服用藥物駕駛之處罰。
二、但經尿液或血液中檢測有\"毒品、迷幻藥、麻醉藥品及其相類似之管制藥品\"成分時，則屬於刑法185-3條第1項「服用毒品、麻醉藥品或其他相類之物，致不能安全駕駛」，此情況建議將行為人(駕駛人)精神狀況以攝影器材紀錄，如可製作觀測表之情況則更好。""",
        quick_reply=QuickReply(
            items=[
            QuickReplyButton(action=MessageAction(label="慢車定義", text="SMV Definition")), 
            QuickReplyButton(action=MessageAction(label="道交條例73條2項及3項", text="Check 73-2 and 73-3")),
            QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode")),
            QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
            ]
            )
        )
    return reply
def dwimode_SMV(event):
    reply = TemplateSendMessage(alt_text="慢車酒駕違規態樣",
        template=ButtonsTemplate(
            title="慢車酒駕違規態樣",
            text='點選違規態樣',
            actions=[
                MessageAction(
                    label="超標舉發",
                    text="Exceed The Maximum Tolerate Standard"
                    ),
                MessageAction(
                    label="拒測舉發",
                    text='Refuses To Take The Test'
                    ),
                MessageAction(
                    label="上一步",
                    text="Back to dwimode"
                    ),
                MessageAction(
                    label="離開",
                    text='Exit'
                    )
            ]
        ))
    return reply
def dwimode_SMV_Ex(event):
    reply = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=[
            CarouselColumn(
                title='慢車行為人-駕駛人(酒駕超標)',
                text='慢車「沒有」累犯規定',
                actions=[
                    MessageAction(
                        label='舉發規定',
                        text='Violation'
                        ),
                    MessageAction(
                        label='慢車定義',
                        text='SMV Definition'
                        ),
                    MessageAction(
                        label='刑法適用問題',
                        text='Criminal Code Question'
                        )
                ]
                ),
            CarouselColumn(
                title='其他',
                text=' ',
                actions=[
                    MessageAction(
                        label='轉換至慢車拒測規定',
                        text='Lead To dwimode_SMV_Re'
                        ),
                    MessageAction(
                        label='上一步',
                        text='Back to dwimode_SMV'
                        ),
                    MessageAction(
                        label='離開',
                        text='Exit'
                        )

                ]
                )
                ]
            )
        )
    return reply
def dwimode_SMV_Re(event):
    reply = TemplateSendMessage(
        alt_text = 'Carousel template',
        template = CarouselTemplate(
            columns=[
            CarouselColumn(
                title='慢車行為人-駕駛人(酒駕拒測)',
                text='慢車「沒有」累犯規定',
                actions=[
                    MessageAction(
                        label='拒測規定',
                        text='Violation'
                        ),
                    MessageAction(
                        label='慢車定義',
                        text='SMV Definition'
                        ),
                    MessageAction(
                        label='拒測告知問題',
                        text='SMV Notification'
                        )
                ]
                ),
            CarouselColumn(
                title='其他',
                text=' ',
                actions=[
                    MessageAction(
                        label='轉換至慢車酒測規定',
                        text='Lead To dwimode_SMV_Ex'
                        ),
                    MessageAction(
                        label='上一步',
                        text='Back to dwimode_SMV'
                        ),
                    MessageAction(
                        label='離開',
                        text='Exit'
                        )

                ]
                )
                ]
            )
        )
    return reply
##dwiNdwd zone
##SQL CMD
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hbisksmwaizgve:c13df8043f36aa6c9a985dca8d1d373c60d76453286bcc62f7055958fe799f4d@ec2-34-231-63-30.compute-1.amazonaws.com:5432/dc0ift2b69djpl"
db = SQLAlchemy(app)
def delete_data(uid):
    sql_cmd = "DELETE FROM userstate WHERE  uid ='"+ uid + "'"
    db.engine.execute(sql_cmd)
def keep_state(uid, mode):
    sql_cmd = "INSERT INTO userstate (uid, state) values('" + uid + "','" + mode + "');"
    db.engine.execute(sql_cmd)
def change_state(uid, mode):
    sql_cmd = "UPDATE userstate SET state = '"+ mode +"' WHERE uid = '"+ uid +"'"
    db.engine.execute(sql_cmd)
def change_var(uid, var, msg):
    sql_cmd = "UPDATE userstate SET "+ var + " = '"+ msg +"' WHERE uid = '"+ uid +"'"
    db.engine.execute(sql_cmd)   
def get_var(uid, var):
    sql_cmd = "SELECT "+ var + " FROM userstate  WHERE uid = '"+ uid +"'"
    return list(db.engine.execute(sql_cmd))[0][0]
##SQL CMD
@app.route("/")
def index():
    return render_template("index.html")
line_bot_api = LineBotApi('m2UPwMSn3p4xmDvVQkvo+AFGkZONQ0yKm3vQlm/RKMODbcTLoEPhS3oQNsqmWciOl3+hxaSy1LrUGQAJ0AxbaS2yTchTCy7Ux5gsMQmsUYkQSO27KIeDhR78RcekWmeF/zvvuMsmudmHMc0OdukCuQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('aa64bf9da34389763d2020a499d6d6ec')
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    uid = event.source.user_id
    sql_cmd = "SELECT * from userstate where uid ='"+ uid + "'"
    uid_data = db.engine.execute(sql_cmd)
    datalist = list(uid_data)
    if len(datalist) == 0:
        # reply = TextSendMessage(text="第一次使用吼!，我已經幫你加入了！")
        if  msg == "[關鍵字搜尋模式]":
            keep_state(uid,"txt_mode")
            reply = enter_txt_mode(event)
        elif msg == "[條號搜尋模式]" :
            keep_state(uid,"nos_mode")
            reply = enter_nos_mode(event)
        elif msg == "[[酒(毒)駕專區]]" :
            keep_state(uid,"dwiNdwdenterButtons")
            reply = dwiNdwdenterButtons(event)
        elif msg == "[[應到案日期計算]]":
            today = datetime.datetime.now()
            initialdate = str(today.year - 1911) + '-' + str(today.month) + '-' + str(today.day)
            expiryDate = today + datetime.timedelta(days = 30)
            finalDate = str(expiryDate.year - 1911) + '-' + str(expiryDate.month) + '-' + str(expiryDate.day)
            reply = TextSendMessage(text="今天日期為：\n"+initialdate + "\n應到案日期為：\n" + finalDate + "\n(當場舉發)")
        elif msg == "[[其他交通問題]]":
            keep_state(uid,"QnA")
            reply = Other_QnA(event)
        else :
            reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
            print("有執行到這裡")
    elif len(datalist) != 0 :
        if "reset" in msg :
            delete_data(uid)
            reply = TextSendMessage(text="重新啟動")
            print("有執行到這裡")
        elif msg == 'Previous-nos_mode':
            change_state(uid, "nos_mode")
            reply = TextSendMessage(text="條文搜尋模式。\n先輸入第＿條：")
        elif msg == 'Exit':
            if "nos_mode" in datalist[0][2]:
                reply = TextSendMessage(text="已離開條號搜尋模式。")
            elif "txt_mode" in datalist[0][2]:
                reply = TextSendMessage(text="已離開關鍵字搜尋模式。")
            else :
                reply = TextSendMessage(text="已離開~")
            delete_data(uid)
        elif datalist[0][2] == "QnA":
            if msg == "處罰機關如何判斷？":
                reply = TextSendMessage(text="依據違反道路交通管理事件統一裁罰基準及處理細則第25條規定：\n舉發汽車違反道路交通管理事件，以汽車所有人為處罰對象者，移送其車籍地處罰機關處理；以駕駛人或乘客為處罰對象者，移送其駕籍地處罰機關處理；駕駛人或乘客未領有駕駛執照者，移送其戶籍地處罰機關處理。但有下列情形之一者，移送行為地處罰機關處理：\n一、汽車肇事致人傷亡。\n二、抗拒稽查致傷害。\n三、汽車駕駛人或乘客未領有駕駛執照且無法查明其戶籍所在地。\n四、汽車買賣業或汽車修理業違反本條例第五十七條規定。\n五、汽車駕駛人違反本條例第三十五條規定。\n計程車駕駛人有本條例第三十六條或第三十七條之情形，應受吊扣執業登記證或廢止執業登記處分者，移送其辦理執業登記之警察機關處理。\n以大眾捷運系統營運機構為被通知人舉發違反道路交通管理事件者，移送其營運機構監督機關所在地處罰機關處理。")
            elif msg == "哪些違規不得郵繳？":
                reply = TextSendMessage(text="依交通部108.07.16.交路字第1080021339號函，不得郵繳的有：\n第12條\n第13條\n第15條第1項第2款、第5款\n第16條第1項第5款\n第17條\n第17條\n第18-1條\n第20條\n第21條\n第21-1條之\n第23條\n第24條\n第26條\n第27條第2項\n第29條第4項\n第29-2條第3項、第5項\n第30條第3項\n第31條第4項\n第34條後段\n第35條第1項至第5項、第7項\n第36條第2項、第3項\n第37條\n第43條\n第45條第2項、第3項\n第54條\n第60條第1項\n第61條\n第62條第1項、第4項及第5項"
                    )
            else:
                reply = TextSendMessage(text="已跳出，請自選單重新開始。")
            delete_data(uid)
        elif datalist[0][2] == "nos_mode":
            if "項" in "".join(search.getListByNos(msg)):
                change_var(uid, 'a', msg)
                change_state(uid, "nos_mode+P")
                reply = selects_nos_mode_P(event,uid,get_var(uid, 'a'))
            elif "項" not in "".join(search.getListByNos(msg)) and "款" in "".join(search.getListByNos(msg)):
                change_var(uid,'a', msg)
                change_state(uid, "nos_mode+S")
                reply = selects_nos_mode_S(event,uid,get_var(uid, 'a'))
            elif "項" not in "".join(search.getListByNos(msg)) and "款" not in "".join(search.getListByNos(msg)) and search.getListByNos(msg) != []:
                change_var(uid, 'a', msg)
                reply = TextSendMessage(text=search.getByNos(get_var(uid,'a')))
                delete_data(uid)
            elif search.getListByNos(msg) == [] :
                reply = TextSendMessage(text="本系統以裁罰基準表內容為主，如查不到法條請上全國法規網。")
                delete_data(uid) 
        elif datalist[0][2] == "nos_mode+P":
            if msg == "列出第"+get_var(uid, 'a')+"條的所有法條":
                reply = TextSendMessage(text=search.getByNos(get_var(uid, 'a')))
                delete_data(uid)
            elif "款" not in "".join(search.getListByNos(get_var(uid, 'a')+','+ msg)):
                reply = TextSendMessage(text=search.getByNos(get_var(uid,'a')+ ','+ msg))
                delete_data(uid)
            else:
                change_var(uid,'p',msg)
                change_state(uid, "nos_mode+P+S")
                reply = selects_nos_mode_P_S(event,uid,get_var(uid, 'a'),get_var(uid, 'p'))
        elif datalist[0][2] == "nos_mode+P+S":
            if msg == "第"+get_var(uid, 'a')+"條第"+get_var(uid, 'p')+"項的所有法條" :
                reply = TextSendMessage(text=search.getByNos(get_var(uid, 'a')+','+get_var(uid,'p')))
                delete_data(uid)
            elif msg == "Previous-nos_mode_P":
                change_state(uid, "nos_mode+P")
                reply = selects_nos_mode_P(event,uid,get_var(uid, 'a'))
            else:
                change_var(uid,'s',msg)
                reply = TextSendMessage(text=search.getByNos(get_var(uid,'a')+ ',' +get_var(uid,'p')+ ','+get_var(uid,'s')))
                delete_data(uid)
        elif datalist[0][2] == "nos_mode+S":
            change_var(uid,'s',msg)
            reply = TextSendMessage(text=search.getByNos(get_var(uid,'a')+',,'+get_var(uid,'s')))
            delete_data(uid)
        elif datalist[0][2] == "txt_mode":
            msg = msg.replace("駕照","駕駛執照")
            msg = msg.replace("車牌","牌照")
            msg = msg.replace("號牌","牌照")
            msg = msg.replace("臨停","臨時停車")
            msg = msg.replace("違停","停車")
            if "兩段" in msg :
                if "慢車" in msg :
                    result  =search.getByNos("73,1,3")
                else:
                    result = search.getByNos("48,1,2") + "\n" +search.getByNos("73,1,3")
            elif "逆向" in msg :
                if ("停車" in msg or "臨時停車" in msg) and "逆向" in msg :
                    msg = msg.replace("逆向","")
                    msg += " 順行"
                    result = search.NosFiltWords("55",msg)+"\n" + search.NosFiltWords("56",msg)+"\n" + search.getByNos("73,1,3")+"\n" + search.getByNos("74,1,4")
                elif "行駛" in msg and "逆向" in msg :
                    result = search.getByNos("45,1,1") + "\n" + search.getByNos("45,1,3") + "\n" +search.NosFiltWords("74,1,2",msg)
                else:
                    msg = msg.replace("逆向","")
                    result = search.NosFiltWords("45,1,1",msg)+"\n" + search.NosFiltWords("45,1,3",msg)+"\n" +search.NosFiltWords("55,,4",msg)+"\n" + search.NosFiltWords("56,1,6",msg) + "\n" + search.NosFiltWords("73,1,3",msg)+"\n" + search.NosFiltWords("74,1,2",msg)+"\n" + search.NosFiltWords("73,1,3",msg).strip()
            elif "牌照" in msg:
                result = search.NosFiltWords("12",msg) + "\n" + search.NosFiltWords("13",msg) + "\n" + search.NosFiltWords("14",msg) + "\n" + search.NosFiltWords("15",msg)
            elif "紅" in msg:
                if "右" in msg:
                    if "慢" in msg:
                        result = search.getByNos("74,1,1")
                    elif "汽車" in msg or "機車" in msg:
                        result = search.getByNos("53,2")
                    elif "大眾" in msg:
                        result = search.getByNos("53-1,2")
                    else :
                        result = search.getByNos("53,2") + "\n" + search.getByNos("53-1,2") + "\n" + search.getByNos("74,1,1")
                elif "闖" in msg:
                    if "慢" in msg:
                        result = search.getByNos("74,1,1")
                    elif "汽車" in msg or "機車" in msg:
                        result = search.getByNos("53,1")
                    elif "大眾" in msg:
                        result = search.getByNos("53-1,1")
                    else :
                        result = search.getByNos("53,1") + "\n" + search.getByNos("53-1,1") + "\n" + search.getByNos("74,1,1")
                elif "慢" in msg:
                    result = search.getByNos("74,1,1")
                elif "汽車" in msg or "機車" in msg:
                    result = search.getByNos("53")
                else :
                    result = search.getByNos("53") + search.getByNos("53-1")+ "\n" + search.getByNos("74,1,1")
            elif "方向燈" in msg or "大燈" in msg or "霧燈" in msg :
                result = search.getByNos("42")
            elif "危險駕駛" in msg or "危駕" in msg or "危險駕車" in msg or "超速" in msg :
                if "超速" in msg :
                    msg = msg.replace("超速","")
                    result = search.NosFiltWords("40",msg + "時速") + "\n" + search.NosFiltWords("43,1",msg) + "\n" + search.NosFiltWords("72-1",msg)
                elif "慢車" in msg :
                    result = search.getByNos("72-1")
                else :
                    msg = msg.replace("危險駕駛","")
                    msg = msg.replace("危駕","")
                    msg = msg.replace("危險駕車","")
                    result = search.getByNos("43") + "\n" +search.getByNos("73,1,4")
                reply = TextSendMessage(text=result)
            elif "酒駕" in msg or "毒駕" in msg or "毒" in msg or "拒測" in msg :
                msg = msg.replace("累犯","累")
                msg = msg.replace("累","年內")
                if "拒測" in msg :
                    msg = msg.replace("拒測","")
                    msg = msg.replace("酒駕","")
                    msg = msg.replace("毒駕","毒")
                    msg = msg.replace("毒","藥")
                    msg = msg.replace("拒測","")
                    result = search.NosFiltWords("35,4",msg) + "\n" + search.NosFiltWords("35,5",msg) + "\n" + search.NosFiltWords("73,3",msg)
                elif "酒駕" in msg:
                    msg = msg.replace("酒駕","")
                    result = search.NosFiltWords("35,1",msg) + "\n" + search.NosFiltWords("35,3",msg) + "\n" + search.NosFiltWords("35,7",msg) + "\n" + search.NosFiltWords("35,8",msg) + "\n" + search.NosFiltWords("73,2",msg)
                elif "毒駕" in msg or "毒" in msg:
                    msg = msg.replace("毒駕","毒")
                    msg = msg.replace("毒","")
                    result = search.NosFiltWords("35,1",msg + " 藥") + "\n" + search.NosFiltWords("35,3",msg) + "\n" + search.NosFiltWords("35,7",msg)
            elif "酒精" in msg and "鎖" in msg :
                msg = msg.replace("酒精","")
                msg = msg.replace("鎖","")
                result = search.NosFiltWords("35-1",msg + " 車輛點火自動鎖定裝置")
            elif "無照" in msg :
                msg = msg.replace("無照"," 未領有駕駛執照駕")
                if "動力" in msg :
                    result = search.getByNos("32,1")
                elif "大型" in msg:
                    result = search.Content_finder(msg) + "\n" + search.NosFiltWords("92,7,3",msg)
                else:
                    result = search.Content_finder(msg) + "\n" + search.NosFiltWords("32,1",msg)+ "\n" + search.NosFiltWords("92,7,3",msg)
            elif "越級" in msg:
                msg = msg.replace("越級"," 領有")
                result = search.dContent_finder(msg,"未領有 未符 未依規定 號牌")
            elif "不服稽查" in msg:
                msg = msg.replace("不服稽查","")
                result = search.NosFiltWords("60,1",msg) + "\n" + search.NosFiltWords("60,2,1",msg)
            else:
                result = search.Content_finder(msg)
                if len(result.replace("\n","").replace(" ","")) == 0 :
                    result = "本系統以裁罰基準表內容為主，如查不到法條請上全國法規網。"
                elif len(result.replace("\n","").replace(" ","")) > 5000:
                    result = "查詢的內容太多了，請重新輸入關鍵字。"
                else:
                    pass
            delete_data(uid)
            try:
                result = result.lstrip().strip()
            except:
                pass
            reply = TextSendMessage(text=result)
        elif datalist[0][2] == "dwiNdwdenterButtons":#酒毒駕進入面板
            if "DWI and DUD" in msg:
                reply = dwiNdwd(event)
                change_state(uid, "dwiNdwd")
            elif "The Newist Announcement" in msg:
                reply = ImageSendMessage(
                    original_content_url='https://raw.githubusercontent.com/laya1017/image/main/newisetAct.jpg',
                    preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/newisetAct.jpg')
                delete_data(uid) #進入版面
            elif msg == "汽機車酒駕法條":
                reply = TextSendMessage(
                    text=search.getByNos("35,1,1"),
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "汽機車毒駕法條":
                reply = TextSendMessage(
                    text=search.getByNos("35,1,2"),
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "累犯法條":
                reply = TextSendMessage(
                    text=search.getByNos("35,3"),
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "汽機車酒駕拒測法條":
                reply = TextSendMessage(
                    text=search.getByNos("35,4"),
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "拒測累犯法條":
                reply = TextSendMessage(
                    text=search.getByNos("35,5"),
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "汽機車酒駕拒測告知":
                reply = TextSendMessage(
                    text="""一、告知拒測之法律效果：
 1.拒絕接受酒精濃度測試檢定者，處新臺幣18萬元罰鍰，並吊銷駕駛執照及吊扣該車輛牌照2年。肇事致人重傷或死亡者，並得沒入車輛。
 2.10年內第2次違反本條例第35條第4項規定者，處新臺幣36萬元罰鍰；第3次以上者按前次違反拒測規定所處罰鍰金額加罰新臺幣18萬元，吊銷駕駛執照，公路主管機關得公布姓名、照片及違法事實，並吊扣該車輛牌照二年；肇事致人重傷或死亡者，並得沒入車輛。
 3.租賃車業者已盡告知本條例第三十五條處罰規定之義務，汽車駕駛人仍有前者之情形，依所處罰鍰加罰二分之一。
 二、依據違反道路交通管理事件統一裁罰基準及處理細則第19-2條第5項，須告知法律效果之情形為\"拒絕配合實施第35條第1項第1款檢測\"，除此之外情形不適用此規定。""",
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "慢車酒駕法條":
                reply = TextSendMessage(
                    text=search.getByNos("73,2"),
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "慢車酒駕拒測法條":
                reply = TextSendMessage(
                    text=search.getByNos("73,3"),
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "自動點火裝置(酒精鎖)":
                reply = TextSendMessage(
                    text=search.getByNos("35-1"),
                    quick_reply=dwiNdwdbuttonFilt(msg)
                    )
            elif msg == "回到酒(毒)駕區":
                reply = dwiNdwdenterButtons(event, msg)
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
        elif datalist[0][2] == "dwiNdwd": #酒駕與毒駕
            if msg == "DWI Regulation":
                reply = dwimode(event)
                change_state(uid, "dwimode") #酒駕規定區
            elif msg == "DWD Regulation":
                reply = dwdmode(event)
                change_state(uid, "dwdmode") #毒駕規定區
            elif msg == "Back to dwiNdwdenterButtons":
                change_state(uid, "dwiNdwdenterButtons")
                reply = dwiNdwdenterButtons(event,msg) #回到進入面板
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
        elif datalist[0][2] == "dwimode" : #酒駕規定區
            if msg == "Cars and Scooters":
                reply = dwimode_CNS(event)
                change_state(uid, "dwimode_CNS")
            elif msg == "Slow-moving vehicles":
                reply = dwimode_SMV(event)
                change_state(uid, "dwimode_SMV")
            elif msg == "Back to dwiNdwd":                
                reply = dwiNdwd(event)
                change_state(uid, "dwiNdwd")
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
        elif datalist[0][2] == "dwimode_CNS": #酒駕汽機車違規態樣
            if msg == "Exceed The Maximum Tolerate Standard":
                reply = dwimode_CNS_Ex(event) #進入汽機車酒駕超標面板
                change_state(uid, "dwimode_CNS_Ex")
            elif msg == "Refuses To Take The Test":
                reply = dwimode_CNS_Re(event) #進入汽機車拒測面板
                change_state(uid, "dwimode_CNS_Re")
            elif msg == "Back to dwimode":
                reply = dwimode(event) #回到酒駕規定區
                change_state(uid, "dwimode")
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
        elif datalist[0][2] == "dwimode_CNS_Ex": #酒駕超標舉發
            if msg == "First Violation":
                reply = TextSendMessage(
                    text=search.getByNos('35,1,1').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與慢車酒駕比較",text="SMV Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Recidivism":
                reply = TextSendMessage(
                    text=search.getByNos('35,3').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Dos and Don\'ts":
                reply = TextSendMessage(
                    text = """一、檢測流程：
1.原則於現場攔檢測試。如現場無法或不宜實施檢測時，得向受測者說明，請其至勤務處所或適當場所檢測。
2.詢問飲用酒類結束時間，如已達十五分鐘以上者，即予檢測。
3.受測者不告知時間或距結束時間未達15分鐘者，告知其可於漱口或距該結束時間達15分鐘後進行檢測。
4.有請求漱口者，提供漱口。
5.告知受測者儀器檢測之流程，請其口含吹嘴連續吐氣至儀器顯示取樣完成。
6.受測者吐氣不足致儀器無法完成取樣時，應重新檢測。
7.因儀器問題或受測者未符合檢測流程，致儀器檢測失敗，應向受測者說明檢測失敗原因，請其重新接受檢測。
8.檢測成功後，不論有無超過規定標準，不得實施第二次檢測。
9.遇檢測結果出現明顯異常情形時，應停止使用該儀器並改用其他儀器檢測，並應留存原異常之紀錄。
10.檢測後，應告知受測者檢測結果，並請其於檢測結果紙上簽名確認。
11.拒絕簽名時，應記明事由。
12.有客觀事實足認受測者無法實施吐氣酒精濃度檢測時，得經其同意後送由受委託醫療或檢驗機構對其實施血液之採樣及測試檢定。
二、標準值：
1.道安規則114條：飲用酒類或其他類似物後其吐氣所含酒精濃度達0.15mgl或血液中酒精濃度達0.03%以上。
2.刑法185-3條："吐氣所含酒精濃度達0.25mg/l或血液中酒精濃度達0.05%以上"
三、勸導要件：
1.駕駛汽車或慢車經測試檢定，其吐氣所含酒精濃度超過規定之標準值(0.15mgl或血液中酒精濃度達0.03%)未逾0.02mg/l。
2.行為人發生交通事故時，仍得舉發。
四、租賃車部分：
1.租賃車業者已盡告知本條處罰規定之義務，汽機車駕駛人仍駕駛汽機車違反第一項、第三項至第五項規定之一者，依其各行為所處之罰鍰加罰1/2。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Owner":
                reply = TextSendMessage(
                    text=search.getByNos('35,7').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Passenger":
                reply = TextSendMessage(
                    text=search.getByNos('35,8').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Impunity Condition":
                reply = TextSendMessage(
                    text="但年滿七十歲、心智障礙或汽車運輸業之乘客，不在此限。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Back to dwimode_CNS_Ex":
                reply = dwimode_CNS_Ex(event)
            elif msg == "Lead To dwimode_CNS_Re": 
                reply = dwimode_CNS_Re(event)
                change_state(uid, "dwimode_CNS_Re")
            elif msg == "Back to dwimode_CNS":
                reply = dwimode_CNS(event)
                change_state(uid, "dwimode_CNS")
            elif msg == "SMV Violation":
                reply = TextSendMessage(
                    text=search.getByNos("73,2"),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
        elif datalist[0][2] == "dwimode_CNS_Re":#汽機車拒測舉發
            if msg == "First Violation":
                reply = TextSendMessage(
                    text=search.getByNos('35,4').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與慢車拒測比較",text="SMV Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "SMV Violation":
                reply = TextSendMessage(
                    text=search.getByNos("73,3").strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Recidivism":
                reply = TextSendMessage(
                    text=search.getByNos('35,5').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Notification":
                reply = TextSendMessage(
                    text = """一、告知拒測之法律效果：
 1.拒絕接受酒精濃度測試檢定者，處新臺幣18萬元罰鍰，並吊銷駕駛執照及吊扣該車輛牌照2年。肇事致人重傷或死亡者，並得沒入車輛。
 2.10年內第2次違反本條例第35條第4項規定者，處新臺幣36萬元罰鍰；第3次以上者按前次違反拒測規定所處罰鍰金額加罰新臺幣18萬元，吊銷駕駛執照，公路主管機關得公布姓名、照片及違法事實，並吊扣該車輛牌照二年；肇事致人重傷或死亡者，並得沒入車輛。
 3.租賃車業者已盡告知本條例第三十五條處罰規定之義務，汽車駕駛人仍有前者之情形，依所處罰鍰加罰二分之一。
 二、依據違反道路交通管理事件統一裁罰基準及處理細則第19-2條第5項，須告知法律效果之情形為\"拒絕配合實施第35條第1項第1款檢測\"，除此之外情形不適用此規定。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="參閱細則19-2條規定", text="Refer 19-2")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Refer 19-2":
                reply = TextSendMessage(
                    text = """
I  .對汽車駕駛人實施本條例第三十五條第一項第一款測試之檢定時，應以酒精測試儀器檢測且實施檢測過程應全程連續錄影，並依下列程序處理：
一、實施檢測，應於攔檢現場為之。但於現場無法或不宜實施檢測時，得向受測者說明，請其至勤務處所或適當場所檢測。
二、詢問受測者飲用酒類或其他類似物結束時間，其距檢測時已達十五分鐘以上者，即予檢測。但遇有受測者不告知該結束時間或距該結束時間未達十五分鐘者，告知其可於漱口或距該結束時間達十五分鐘後進行檢測；有請求漱口者，提供漱口。
三、告知受測者儀器檢測之流程，請其口含吹嘴連續吐氣至儀器顯示取樣完成。受測者吐氣不足致儀器無法完成取樣時，應重新檢測。
四、因儀器問題或受測者未符合檢測流程，致儀器檢測失敗，應向受測者說明I２.檢測失敗原因，請其重新接受檢測。
II .實施前項檢測後，應告知受測者檢測結果，並請其在儀器列印之檢測結果紙上簽名確認。拒絕簽名時，應記明事由。
III.實施第一項檢測成功後，不論有無超過規定標準，不得實施第二次檢測。但遇檢測結果出現明顯異常情形時，應停止使用該儀器，改用其他儀器進行檢測，並應留存原異常之紀錄。
IV .有客觀事實足認受測者無法實施吐氣酒精濃度檢測時，得於經其同意後，送由受委託醫療或檢驗機構對其實施血液之採樣及測試檢定。
V  .汽車駕駛人拒絕配合實施本條例第三十五條第一項第一款檢測者，應依下列規定處理：
一、告知拒絕檢測之法律效果：
（一）拒絕接受酒精濃度測試檢定者，處新臺幣十八萬元罰鍰，吊銷駕駛執照及吊扣該車輛牌照二年；肇事致人重傷或死亡者，並得沒入車輛。
（二）於十年內第二次違反本條例第三十五條第四項規定者，處新臺幣三十六萬元罰鍰，第三次以上者按前次違反本項所處罰鍰金額加罰新臺幣十八萬元，吊銷駕駛執照，公路主管機關得公布姓名、照片及違法事實，並吊扣該車輛牌照二年；肇事致人重傷或死亡者，並得沒入車輛。
（三）租賃車業者已盡告知本條例第三十五條處罰規定之義務，汽車駕駛人仍有前二目情形者，依所處罰鍰加罰二分之一。
二、依本條例第三十五條第四項或第五項製單舉發。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Back to dwimode_CNS":
                reply = dwimode_CNS(event)
                change_state(uid, "dwimode_CNS")
            elif msg == "Lead To dwimode_CNS_Ex":
                reply = dwimode_CNS_Ex(event)
                change_state(uid, "dwimode_CNS_Ex")
            elif msg == "Back to dwimode_CNS_Re":
                reply = dwimode_CNS_Re(event)
            elif msg == "Back to dwimode":
                reply = dwimode(event) #回到酒駕規定區
                change_state(uid, "dwimode")
        elif datalist[0][2] == "dwimode_SMV": #酒駕慢車
            if msg == "Exceed The Maximum Tolerate Standard":
                reply = dwimode_SMV_Ex(event) #進入慢車酒駕超標面板
                change_state(uid, "dwimode_SMV_Ex")
            elif msg == "Refuses To Take The Test":
                reply = dwimode_SMV_Re(event) #進入慢車拒測面板
                change_state(uid, "dwimode_SMV_Re")
            elif msg == "Back to dwimode":
                reply = dwimode(event) #回到酒駕規定區
                change_state(uid, "dwimode")
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
        elif datalist[0][2] == "dwimode_SMV_Ex": #慢車超標舉發
            if msg == "Violation":
                reply = TextSendMessage(
                    text=search.getByNos("73,2"),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與汽機車酒駕規定比較", text="CNS Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "CNS Violation":
                reply = TextSendMessage(
                    text=search.getByNos('35,1,1').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "SMV Definition":
                reply = TextSendMessage(
                    text="""道交條例69條1項：
慢車種類及名稱如下：
一、自行車：
（一）腳踏自行車。
（二）電動輔助自行車：指經型式審驗合格，以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。
（三）電動自行車：指經型式審驗合格，以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。
二、其他慢車：
（一）人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。
（二）獸力行駛車輛：指牛車、馬車等。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Criminal Code Question":
                reply = TextSendMessage(
                    text="""依據法務部法檢字第1000014063號函：
要旨：
參照刑法第 185條之 3規定，「腳踏自行車」「電動輔助自行車」「電動自行車」是否符合該條之「動力交通工具」，端視其推動是否以電力或引擎動力等作用而斷
主旨：就所詢刑法第 185條之 3「動力交通工具」之適用範圍乙案，復如說明，請查照。
說明：
一、復貴署100年5月23日警署交字第1000117598號函。
二、刑法第185條之3之「動力交通工具」，係指交通工具之推動是以電力或引擎動力等作用者，至其為蒸汽機、內燃機，抑或係柴油、汽油、天然氣、核子、電動，均非所問。又所謂交通工具不限於陸路交通工具，尚包含水上、海上、空中或鐵道上之交通工具。所詢之「腳踏自行車」「電動輔助自行車」「電動自行車」是否符合刑法第185條之3之「動力交通工具」，端視其推動是否以電力或引擎動力等作用而斷。惟如涉及具體個案，應由承辦之檢察官或法官依職權判斷。
正本：內政部警政署
副本：本部檢察司、本部檢察司一股""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Lead To dwimode_SMV_Re":
                reply = dwimode_SMV_Re(event)
                change_state(uid, "dwimode_SMV_Re")
            elif msg == "Back to dwimode_SMV":
                reply = dwimode_SMV(event)
                change_state(uid, "dwimode_SMV")
            elif msg == "dwimode_SMV_Ex":
                reply = dwimode_SMV_Ex(event)
        elif datalist[0][2] == "dwimode_SMV_Re":
            if msg == "Violation":
                reply = TextSendMessage(
                    text=search.getByNos('73,3').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與汽機車拒測規定比較", text="CNS Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "CNS Violation":
                reply = TextSendMessage(
                    text=search.getByNos('35,4').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "SMV Definition":
                reply = TextSendMessage(
                    text="""道交條例69條1項：
慢車種類及名稱如下：
一、自行車：
（一）腳踏自行車。
（二）電動輔助自行車：指經型式審驗合格，以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。
（三）電動自行車：指經型式審驗合格，以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。
二、其他慢車：
（一）人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。
（二）獸力行駛車輛：指牛車、馬車等。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "SMV Notification":
                reply = TextSendMessage(
                    text="""依目前違反道路交通管理事件統一裁罰基準及處理細則第19-2條並無相關規定。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Lead To dwimode_SMV_Ex":
                reply = dwimode_SMV_Ex(event)
                change_state(uid, "dwimode_SMV_Ex")
            elif msg == "Back to dwimode_SMV":
                reply = dwimode_SMV(event)
                change_state(uid, "dwimode_SMV")
            elif msg == "dwimode_SMV_Re":
                reply = dwimode_SMV_Re(event)
        elif datalist[0][2] == "dwdmode" : #毒駕規定區
            if msg == "Cars and Scooters":
                reply = dwdmode_CNS(event)
                change_state(uid, "dwdmode_CNS") #汽機車毒駕違規態樣
            elif msg == "SMV No DWD":
                reply = dwdmode_SMV(event)
                change_state(uid, "dwdmode_SMV") #慢車毒駕面板
            elif msg == "Back to dwiNdwd":
                reply = dwiNdwd(event)
                change_state(uid, "dwiNdwd") #回到酒駕與毒駕選擇版面
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
        elif datalist[0][2] == "dwdmode_CNS": #汽機車毒駕違規態樣
            if msg == "Exceed The Maximum Tolerate Standard":
                reply = dwdmode_CNS_Ex(event) #進入汽機車毒駕超標面板
                change_state(uid, "dwdmode_CNS_Ex")
            elif msg == "Refuses To Take The Test":
                reply = dwdmode_CNS_Re(event) #進入汽機車拒測面板
                change_state(uid, "dwdmode_CNS_Re")
            elif msg == "Back to dwdmode":
                reply = dwdmode(event) #回到汽機車毒駕面板
                change_state(uid, "dwdmode")
        elif datalist[0][2] == "dwdmode_CNS_Ex": #毒駕超標舉發
            if msg == "First Violation":
                reply = TextSendMessage(
                    text=search.getByNos('35,1,2').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="慢車沒有毒駕處罰？",text="SMV Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "SMV Violation":
                reply = TextSendMessage(
                    text="""一、慢車於道路交通管理處罰條例第73條2項及3項皆處罰為「\"酒精\"濃度超標」及「拒絕\"酒精\"濃度測試」，且於同法中並\"無\"規定服用藥物駕駛之處罰。
二、但經尿液或血液中檢測有\"毒品、迷幻藥、麻醉藥品及其相類似之管制藥品\"成分時，則屬於刑法185-3條第1項「服用毒品、麻醉藥品或其他相類之物，致不能安全駕駛」，此情況建議將行為人(駕駛人)精神狀況以攝影器材紀錄，如可製作觀測表之情況則更好。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="道交條例73條2項及3項", text="Check 73-2 and 73-3")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Check 73-2 and 73-3":
                reply = TextSendMessage(
                    text=search.getByNos("73,2")+"\n"+search.getByNos("73,3").strip(),
                    quick_reply = QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="回上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Recidivism":
                reply = TextSendMessage(
                    text=search.getByNos('35,3').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Dos and Don\'ts":
                reply = TextSendMessage(
                    text = """一、標準值(供參考用)：
濫用藥物尿液檢驗作業準則18條：
I 初步檢驗結果在閾值以上或有疑義之尿液檢體，應再進行確認檢驗。確認檢驗結果在下列閾值以上者，應判定為陽性：
1、安非他命類藥物：
（1）安非他命：500ng/mL。
（2）甲基安非他命：甲基安非他命500ng/mL，且其代謝物安非他命之濃度在100ng/mL以上。
（3）3,4-亞甲基雙氧甲基安非他命（MDMA）：500ng/mL。同時檢出MDMA及MDA時，兩種藥物之個別濃度均低於500ng/mL，但總濃度在500ng/mL以上者，亦判定為MDMA陽性。
（4）3,4-亞甲基雙氧安非他命（MDA）：500ng/mL。
（5）3,4-亞甲基雙氧-N-乙基安非他命（MDEA）：500ng/mL。
2、海洛因、鴉片代謝物：
（1）嗎啡：300ng/mL。
（2）可待因：300ng/mL。
3、大麻代謝物（四氫大麻酚-9-甲酸，Delta-9-tetrahydrocannabinol-9-carboxylicacid）：15ng/mL。
4、古柯鹼代謝物（苯甲醯基愛哥寧，Benzoylecgonine）：150ng/mL。
5、愷他命代謝物：
（一）愷他命（Ketamine）：100ng/mL。同時檢出愷他命及去甲基愷他命（Norketamine）時，兩種藥物之個別濃度均低於100ng/mL，但總濃度在100ng/mL以上者，亦判定為愷他命陽性。
（二）去甲基愷他命：100ng/mL。
II、前項以外之濫用藥物或其代謝物，依衛生福利部食品藥物管理署公告之濃度作為判定檢出之閾值。未有公告者，檢驗機構得依其分析方法最低可定量濃度訂定適當閾值。
二、建議：
此情況建議施測前將行為人(駕駛人)精神狀況以攝影器材紀錄、製作觀測表，如涉嫌隨案移請地方檢察署檢察官認定。
三、租賃車部分：
1.租賃車業者已盡告知本條處罰規定之義務，汽機車駕駛人仍駕駛汽機車違反第一項、第三項至第五項規定之一者，依其各行為所處之罰鍰加罰1/2。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Owner":
                reply = TextSendMessage(
                    text=search.getByNos('35,7').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Passenger":
                reply = TextSendMessage(
                    text="道交條例第35條第8項規定為\"酒精\"濃度超標，並\"無\"服用藥物之同車乘客處罰。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="參考法條35條8項", text="Check 35-8")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Check 35-8":
                reply = TextSendMessage(
                    text=search.getByNos("35,8"),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Impunity Condition":
                reply = TextSendMessage(
                    text="道交條例第35條第8項規定為\"酒精\"濃度超標，並\"無\"服用藥物之同車乘客處罰。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="參考法條35條8項", text="Check 35-8")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Back to dwdmode_CNS_Ex":
                reply = dwdmode_CNS_Ex(event)
            elif msg == "Lead To dwdmode_CNS_Re": 
                reply = dwdmode_CNS_Re(event)
                change_state(uid, "dwdmode_CNS_Re")
            elif msg == "Back to dwdmode_CNS":
                reply = dwdmode_CNS(event)
                change_state(uid, "dwdmode_CNS")
            elif msg == "SMV Violation":
                reply = TextSendMessage(
                    text=search.getByNos("73,2"),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
        elif datalist[0][2] == "dwdmode_CNS_Re":
            if msg == "First Violation":
                reply = TextSendMessage(
                    text=search.getByNos('35,4').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與慢車拒測比較",text="SMV Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "SMV Violation":
                reply = TextSendMessage(
                    text=search.getByNos("73,3").strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Recidivism":
                reply = TextSendMessage(
                    text=search.getByNos('35,5').strip(),
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Notification":
                reply = TextSendMessage(
                    text = "依據違反道路交通管理事件統一裁罰基準及處理細則第19-2條第5項，須告知法律效果之情形為\"拒絕配合實施第35條第1項第1款檢測\"，故毒駕不適用此規定。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="參閱細則19-2條規定", text="Refer 19-2")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Refer 19-2":
                reply = TextSendMessage(
                    text = """
I  .對汽車駕駛人實施本條例第三十五條第一項第一款測試之檢定時，應以酒精測試儀器檢測且實施檢測過程應全程連續錄影，並依下列程序處理：
一、實施檢測，應於攔檢現場為之。但於現場無法或不宜實施檢測時，得向受測者說明，請其至勤務處所或適當場所檢測。
二、詢問受測者飲用酒類或其他類似物結束時間，其距檢測時已達十五分鐘以上者，即予檢測。但遇有受測者不告知該結束時間或距該結束時間未達十五分鐘者，告知其可於漱口或距該結束時間達十五分鐘後進行檢測；有請求漱口者，提供漱口。
三、告知受測者儀器檢測之流程，請其口含吹嘴連續吐氣至儀器顯示取樣完成。受測者吐氣不足致儀器無法完成取樣時，應重新檢測。
四、因儀器問題或受測者未符合檢測流程，致儀器檢測失敗，應向受測者說明I２.檢測失敗原因，請其重新接受檢測。
II .實施前項檢測後，應告知受測者檢測結果，並請其在儀器列印之檢測結果紙上簽名確認。拒絕簽名時，應記明事由。
III.實施第一項檢測成功後，不論有無超過規定標準，不得實施第二次檢測。但遇檢測結果出現明顯異常情形時，應停止使用該儀器，改用其他儀器進行檢測，並應留存原異常之紀錄。
IV .有客觀事實足認受測者無法實施吐氣酒精濃度檢測時，得於經其同意後，送由受委託醫療或檢驗機構對其實施血液之採樣及測試檢定。
V  .汽車駕駛人拒絕配合實施本條例第三十五條第一項第一款檢測者，應依下列規定處理：
一、告知拒絕檢測之法律效果：
（一）拒絕接受酒精濃度測試檢定者，處新臺幣十八萬元罰鍰，吊銷駕駛執照及吊扣該車輛牌照二年；肇事致人重傷或死亡者，並得沒入車輛。
（二）於十年內第二次違反本條例第三十五條第四項規定者，處新臺幣三十六萬元罰鍰，第三次以上者按前次違反本項所處罰鍰金額加罰新臺幣十八萬元，吊銷駕駛執照，公路主管機關得公布姓名、照片及違法事實，並吊扣該車輛牌照二年；肇事致人重傷或死亡者，並得沒入車輛。
（三）租賃車業者已盡告知本條例第三十五條處罰規定之義務，汽車駕駛人仍有前二目情形者，依所處罰鍰加罰二分之一。
二、依本條例第三十五條第四項或第五項製單舉發。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Back to dwdmode_CNS":
                reply = dwdmode_CNS(event)
                change_state(uid, "dwdmode_CNS")
            elif msg == "Lead to dwdmode_CNS_Ex":
                print("1504",reply)
                reply = dwdmode_CNS_Ex(event)
                print("1506",reply)
                change_state(uid, "dwdmode_CNS_Ex")
            elif msg == "Back to dwdmode_CNS_Re":
                reply = dwdmode_CNS_Re(event)
            elif msg == "Back to dwdmode":
                reply = dwdmode(event) 
                change_state(uid, "dwdmode")
        elif datalist[0][2] == "dwdmode_SMV":
            if msg == "SMV Definition":
                reply = TextSendMessage(
                    text="""道交條例69條1項：
慢車種類及名稱如下：
一、自行車：
（一）腳踏自行車。
（二）電動輔助自行車：指經型式審驗合格，以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。
（三）電動自行車：指經型式審驗合格，以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。
二、其他慢車：
（一）人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。
（二）獸力行駛車輛：指牛車、馬車等。""",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_SMV")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Check 73-2 and 73-3":
                reply = TextSendMessage(
                    text=search.getByNos("73,2")+"\n"+search.getByNos("73,3").strip(),
                    quick_reply = QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="回上一步", text="Back to dwdmode_SMV")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Back to dwdmode":
                reply = dwdmode(event) #回到汽機車毒駕面板
                change_state(uid, "dwdmode")
            elif msg == "Back to dwdmode_SMV":
                reply = dwdmode_SMV(event)
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
    line_bot_api.reply_message(event.reply_token,reply)

if __name__ == "__main__":
    app.run()

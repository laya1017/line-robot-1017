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
            QuickReplyButton(action=MessageAction(label="駕照", text="駕照")),
            QuickReplyButton(action=MessageAction(label="駕照 吊扣(可改吊銷)", text="駕照 吊扣")),
            QuickReplyButton(action=MessageAction(label="牌照 吊扣(可改吊銷)", text="牌照 吊扣")),
            QuickReplyButton(action=MessageAction(label="酒駕(可加累犯)", text="酒駕")),
            QuickReplyButton(action=MessageAction(label="拒測(可加累犯)", text="拒測")),
            QuickReplyButton(action=MessageAction(label="逆向 行駛(可以改為停車)", text="逆向 行駛")),
            QuickReplyButton(action=MessageAction(label="兩段式", text="兩段式")),
            QuickReplyButton(action=MessageAction(label="紅燈", text="紅燈")),
            QuickReplyButton(action=MessageAction(label="酒精鎖", text="酒精鎖")),
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

##dwiNdwdZone
def dwiNdwdenterButtons(event):
    reply = TemplateSendMessage(alt_text="酒(毒)駕專區",
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

##dwiNdwdZone

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
        elif datalist[0][2] == "dwiNdwdenterButtons":
            if "DWI and DUD" in msg:
                reply = TextSendMessage(text="還在研發中，請見諒。")
                delete_data(uid)
            elif "The Newist Announcement" in msg:
                reply = ImageSendMessage(
                    original_content_url='https://raw.githubusercontent.com/laya1017/image/main/newisetAct.jpg',
                    preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/newisetAct.jpg')
                delete_data(uid)
            elif "Exit" in msg:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
    line_bot_api.reply_message(event.reply_token,reply)

if __name__ == "__main__":
    app.run()

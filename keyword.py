from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackAction,MessageAction,CarouselTemplate,CarouselColumn,QuickReply,QuickReplyButton,FlexSendMessage
)
import search
import pandas as pd
def keywords (msg):
    if "兩段" in msg :
        if "慢車" in msg :
            reply = TextSendMessage(text=search.getByNos("73,1,3"))
        else:
            reply = TextSendMessage(text=search.getByNos("48,1,2")+"\n"+search.getByNos("73,1,3"))
    elif ("分向限制線" in msg and "迴車" in msg) or ("禁止變換車道線" in msg and "迴車" in msg) or "迴車" in msg:
            reply = TextSendMessage(text=search.NosFiltWords("33",msg)+"\n"+search.NosFiltWords("49",msg)+"\n"+search.getByNos("74,1,4"))
    elif "分向限制線" in msg  and "左轉" in msg:
            reply = TextSendMessage(text="交通部94.06.15.交路字第0940035842號函：\n查道路交通管理處罰條例第48條應係對汽車駕駛人行駛至轉彎路段未依規定轉彎之處罰，對於本案臺中縣警察局所提汽車於繪有行車分向限制線段左轉彎，應係未依分向限制線標線規定行駛之違規轉彎行為，此與上述第48條之未依規定轉彎情形，應屬有間，本部同意貴署所提適用處罰條例第60條第2項第3款「不遵守道路交通標線之指示」之處罰。")
    elif "禁止變換車道線" in msg and "跨越" in msg:
            reply = TextSendMessage(text=search.getByNos("45,1,12"))
    elif "逆向" in msg :
        if ("停車" in msg or "臨時停車" in msg) and "逆向" in msg :
            msg = msg.replace("逆向","")
            msg+= " 順行"
            reply = TextSendMessage(text=search.NosFiltWords("55",msg)+"\n"+search.NosFiltWords("56",msg)+"\n"+search.getByNos("73,1,3")+"\n"+search.getByNos("74,1,4"))
        elif "行駛" in msg and "逆向" in msg :
            reply = TextSendMessage(text=search.getByNos("45,1,1")+"\n"+search.getByNos("45,1,3")+"\n"+search.NosFiltWords("74,1,2",msg))
        else:
            msg = msg.replace("逆向","")
            reply = TextSendMessage(text=search.NosFiltWords("45,1,1",msg)+"\n"+search.NosFiltWords("45,1,3",msg)+"\n"+search.NosFiltWords("55,,4",msg)+"\n"+search.NosFiltWords("56,1,6",msg)+"\n"+search.NosFiltWords("73,1,3",msg)+"\n"+search.NosFiltWords("74,1,2",msg)+"\n"+search.NosFiltWords("73,1,3",msg).strip())
    elif "牌照" in msg:
        reply = TextSendMessage(text=search.NosFiltWords("12",msg)+"\n"+search.NosFiltWords("13",msg)+"\n"+search.NosFiltWords("14",msg)+"\n"+search.NosFiltWords("15",msg))
    elif "紅" in msg:
        reply = TextSendMessage(text=search.NosFiltWords("53",msg)+search.NosFiltWords("53-1",msg)+"\n"+search.NosFiltWords("74,1,1",msg)+search.NosFiltWords("78,1,1",msg))
    elif ("方向燈" in msg) or ("大燈" in msg) or ("霧燈" in msg) or ("頭燈" in msg and "開" in msg) or ("頭燈" in msg and "開" in msg) :
        reply = TextSendMessage(text=search.getByNos("42"))
    elif ("危險駕車" in msg or "危險駕駛" in msg or "危駕" in msg) and "超速" in msg:
        reply = TextSendMessage(text=search.getByNos("43,1,2"))
    elif "危險駕車" in msg or "危險駕駛" in msg or "危駕" in msg:
        msg = msg.replace("危險駕車","")
        msg = msg.replace("危險駕駛","")
        msg = msg.replace("危駕","")
        reply = TextSendMessage(text=search.NosFiltWords("43",msg)+"\n"+search.NosFiltWords("73,1,4",msg))
    elif "超重" in msg or "超載" in msg:
        msg = msg.replace("超重","")
        msg = msg.replace("超載","")
        reply = TextSendMessage(text=search.NosFiltWords("29-2,1",msg)+"\n"+search.NosFiltWords("29-2,2",msg))
    elif "機車" in msg and "裝載" in msg:
        reply = TextSendMessage(text=search.getByNos("31,5"))
    elif "拒磅" in msg:
        reply = TextSendMessage(text=search.getByNos("29-2,4"))
    elif "超速" in msg and ("危險駕車" not in msg or "危險駕駛" not in msg or "危駕" not in msg):
        msg = msg.replace("慢車","電動自行車")
        msg = msg.replace("超速","")
        reply = TextSendMessage(text=search.NosFiltWords("40",msg+"最高")+"\n"+search.NosFiltWords("72-1",msg))
    elif "酒駕" in msg or "毒駕" in msg or "毒" in msg or "拒測" in msg :
        msg = msg.replace("累犯","累")
        msg = msg.replace("累","年內")
        if "拒測" in msg :
            msg = msg.replace("拒測","")
            msg = msg.replace("酒駕","")
            msg = msg.replace("毒駕","毒")
            msg = msg.replace("毒","藥")
            msg = msg.replace("拒測","")
            reply = TextSendMessage(text=search.NosFiltWords("35,4",msg)+"\n"+search.NosFiltWords("35,5",msg)+"\n"+search.NosFiltWords("73,3",msg))
        elif "酒駕" in msg:
            msg = msg.replace("酒駕","")
            reply = TextSendMessage(text=search.NosFiltWords("35,1",msg)+"\n"+search.NosFiltWords("35,3",msg)+"\n"+search.NosFiltWords("35,7",msg)+"\n"+search.NosFiltWords("35,8",msg)+"\n"+search.NosFiltWords("73,2",msg))
        elif "毒駕" in msg or "毒" in msg:
            msg = msg.replace("毒駕","毒")
            msg = msg.replace("毒","")
            reply = TextSendMessage(text=search.NosFiltWords("35,1",msg+" 藥")+"\n"+search.NosFiltWords("35,3",msg)+"\n"+search.NosFiltWords("35,7",msg))
    elif "酒精" in msg and "鎖" in msg :
        msg = msg.replace("酒精","")
        msg = msg.replace("鎖","")
        reply = TextSendMessage(text=search.NosFiltWords("35-1",msg+" 車輛點火自動鎖定裝置"))
    elif "無照" in msg :
        msg = msg.replace("無照"," 未領有駕駛執照駕")
        if "動力" in msg :
            reply = TextSendMessage(text=search.getByNos("32,1"))
        elif "大型" in msg:
            reply = TextSendMessage(text=search.Content_finder(msg)+"\n"+search.NosFiltWords("92,7,3",msg))
        else:
            reply = TextSendMessage(text=search.Content_finder(msg)+"\n"+search.NosFiltWords("32,1",msg)+"\n"+search.NosFiltWords("92,7,3",msg))
    elif "越級" in msg:
        msg = msg.replace("越級"," 領有")
        reply = TextSendMessage(text=search.dContent_finder(msg,"未領有 未符 未依規定 號牌"))
    elif "不服稽查" in msg:
        msg = msg.replace("不服稽查","")
        reply = TextSendMessage(text=search.NosFiltWords("60,1",msg)+"\n"+search.NosFiltWords("60,2,1",msg))
    elif ("禁行機車" in msg) or (("機車" in msg) and ("快車道" in msg)):
        reply = TextSendMessage(text=search.getByNos("45,1,13"))
    elif ("左轉" in msg and "車道" in msg) or ("右彎" in msg and "車道" in msg) or ("左彎" in msg and "車道" in msg):
        reply = TextSendMessage(text=search.getByNos("48,1,7"))
    elif ("中心" in msg) and ("彎" in msg):
        reply = TextSendMessage(text=search.getByNos("48,1,3"))
    elif "電動自行車" in msg :
        if search.Content_finder(msg) == "":
            msg.replace("電動自行車","慢車")
            reply = TextSendMessage(text=search.Content_finder(msg))
        else:
            reply = TextSendMessage(text=search.Content_finder(msg))
    elif "電動輔助" in msg :
        if search.Content_finder(msg) == "":
            msg.replace("電動輔助","慢車")
            reply = TextSendMessage(text=search.Content_finder(msg))
        else:
            reply = TextSendMessage(text=search.Content_finder(msg))
    else:
        reply = search.Content_finder(msg)
        if len(result.replace("\n","").replace(" ","")) == 0 :
            reply = FlexSendMessage(alt_text='查無結果',contents=noResult)
        elif len(result.replace("\n","").replace(" ","")) > 5000:
            reply = TextSendMessage(text="查詢的內容太多了，請重新輸入關鍵字。")
        else:
            pass
    try:
        reply.text.lstrip().strip()
    except:
        pass
    if len(reply.text) == 0:
        reply = FlexSendMessage(alt_text='查無結果',contents=noResult)
    reply = Series_Q_Reply(reply)
    return reply
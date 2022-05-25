import pandas as pd
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,
    TemplateSendMessage,ButtonsTemplate,PostbackAction,MessageAction,
    CarouselTemplate,CarouselColumn,QuickReply,QuickReplyButton,
    FlexSendMessage,BubbleContainer,BoxComponent,TextComponent,SeparatorComponent
)
df = pd.read_csv("data.csv")
df.set_index("Nos",inplace = True)
sort = list(df.index)
def getText(_list):
    result_df = df.loc[_list]
    result_text = []
    for i in range(0,len(result_df)):
        result_text.append(result_df.index[i] + "：\n" + result_df["Contents"][i] + "\n處罰：" + result_df["Punishment"][i] + "\n註記：\n" + result_df["Remark"][i].strip("\n") + "\n")
    return "".join(result_text)
def listByArticle(A = ""):
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
def getByNos(Nos):
    keys = Nos.split(",")
    a = keys[0].replace(" ","")
    try:
        p = keys[1].replace(" ","")
    except IndexError:
        p = ""
    try:
        s = keys[2].replace(" ","")
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
    return getText(result).strip("\n")
def getListByNos(Nos):
    keys = Nos.split(",")
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
    return result
def Content_finder(words,temp = df):
    keys = words.split(" ")
    for key in keys :
        condition = temp["Contents"].str.contains(key)
        temp = temp[condition]
    result = []
    for i in range(0,len(temp)):
        result.append(temp.index[i] + "：\n" + temp['Contents'][i] +
             "\n處罰：" + temp["Punishment"][i].strip("\n") + "\n註記：\n" + temp["Remark"][i] + "\n")
    return "".join(result).strip("\n")
def filtDfByWords(words):
    temp = df
    keys = words.split(" ")
    for key in keys :
        condition = temp["Contents"].str.contains(key)
        temp = temp[condition]
    return temp
def filtDfByNos(Nos):
    keys = Nos.split(",")
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
    return df.loc[result]
def filtDfByNosLsit(NosList):
    return df.loc[NosList]
def wordsFiltwords(firstWords,words):
    temp = filtDfByWords(firstWords)
    keys = words.split(" ")
    for key in keys :
        condition = temp["Contents"].str.contains(key)
        temp = temp[condition]
    result = []
    for i in range(0,len(temp)):
        result.append(temp.index[i] + "：\n" + temp['Contents'][i] +
             "\n處罰：" + temp["Punishment"][i].strip("\n") + "\n註記：\n" + temp["Remark"][i] + "\n")
    return "".join(result).strip("\n")
def NosFiltWords(Nos,words):
    temp = filtDfByNos(Nos)
    keys = words.split(" ")
    for key in keys :
        condition = temp["Contents"].str.contains(key)
        temp = temp[condition]
    result = []
    for i in range(0,len(temp)):
        result.append(temp.index[i] + "：\n" + temp['Contents'][i] +
             "\n處罰：" + temp["Punishment"][i].strip("\n") + "\n註記：\n" + temp["Remark"][i] + "\n")
    return "".join(result).strip("\n")
def NosListFiltWords(NosList,words):
    temp = filtDfByNosLsit(NosList)
    keys = words.split(" ")
    for key in keys :
        condition = temp["Contents"].str.contains(key)
        temp = temp[condition]
    result = []
    for i in range(0,len(temp)):
        result.append(temp.index[i] + "：\n" + temp['Contents'][i] +
             "\n處罰：" + temp["Punishment"][i].strip("\n") + "\n註記：\n" + temp["Remark"][i] + "\n")
    return "".join(result).strip("\n")
def getListByWords(words,temp = df):
    keys = words.split(" ")
    for key in keys :
        condition = temp["Contents"].str.contains(key)
        temp = temp[condition]
    result = []
    for i in range(0,len(temp)):
        result.append(temp.index[i])
    lis = []
    for i in result:
        if i not in lis:
            lis.append(i)
    return lis
def dContent_finder(words,dwords,temp = df):
    keys = words.split(" ")
    dkeys = dwords.split(" ")

    for key in keys :
        condition = temp["Contents"].str.contains(key)
        temp = temp[condition]
    for dkey in dkeys :
        dcondition = temp["Contents"].str.contains(dkey)
        temp = temp[dcondition == False]
    result = []
    for i in range(0,len(temp)):
        result.append(temp.index[i] + "：\n" + temp['Contents'][i] +
             "\n處罰：" + temp["Punishment"][i].strip("\n") + "\n註記：\n" + temp["Remark"][i] + "\n")
    return "".join(result).strip("\n")
def setstring(msg,word_list):
    newwords=msg.replace(" ","")
    for i in word_list:
        newwords=newwords.replace(i,"")
    goal=list(newwords)
    for i in word_list:
        if i in msg:
            goal.append(i)
        else:
            pass
    return goal
def D2toD1(d2list,symWords):
    for i in d2list:
        for j in list(symWords.keys()):
            if j == i:
                d2list[d2list.index(i)] = symWords[j]
    comapare_msg = []
    for i in d2list:
        if str(type(i)) == "<class 'list'>":
            for j in i:
                comapare_msg.append(j)
        else:
            comapare_msg.append(i)
    return comapare_msg
def newWordsSearch(msg):
    data = df.copy()
    reply = FlexSendMessage(
        alt_text='關鍵字搜尋結果',
        contents=BubbleContainer(
            size="giga",
            body=BoxComponent(
                layout='vertical',
                contents=[]
                    )
            )
        )
    if "危險駕車" in msg or "危駕" in msg or "危險駕駛" in msg :
        data = df.loc[getListByNos("43")+getListByNos("73,1,4")]
        msg = msg.replace("危險駕車","")
        msg = msg.replace("危駕","")
        msg = msg.replace("危險駕駛","")
    elif "酒" in msg and "駕" in msg:
        data = df.loc[getListByNos("35")+getListByNos("73,2")]
        msg = msg.replace("酒","")
        msg = msg.replace("駕","")
    elif set(msg).issubset(set("雙黃線左轉")):
        data = df.loc[getListByNos("60,2,3")]
        msg = msg.replace("雙黃線左轉","")
    else:
        pass
    word_list = ["駕駛人","救護車","救險車","行人","慢車道","人行","超車","吊銷","註銷","業經","公路","改善","危險物品","有危險","三款","三項","高速公路","傳單"]
    symWords = {
        '機車':["機車",'機','車'],
        '無照':list("駕駛執照"),
        '高、快速公路':["高速公路","快速公路"],
        '變更':list('改裝變更'),
        '駛入':list("行駛入"),
        '犯':list('違反'),
        '未':['未','無','不'],'無':['未','無','不'],'不':['未','無','不'],
        '順行':['順行','逆','向'],'遵行之方向':['逆','向','遵行之方向'],'來車道':['逆','向','來車道'],
        '驟然':list("驟然危險駕駛車"),
        '逾六十公里':list("逾六十公里危險駕駛車"),
        '車輛點火自動鎖定裝置':['酒精鎖']+list('車輛點火自動鎖定裝置'),
        '第四十三條':list("危險駕駛車"),
        '車牌':['號牌','牌照','車牌'],'號牌':['號牌','牌照','車牌'],'牌照':['號牌','牌照','車牌'],
        '雙黃線':['雙黃線','分向限制線','禁止超車線'],'分向限制線':['雙黃線','分向限制線','禁止超車線'],'禁止超車線':['雙黃線','分向限制線','禁止超車線'],
        '迴車':list('迴轉車'),
        '方向燈':['燈','霧燈','方向燈'],'燈':['燈','霧燈','方向燈'],'霧燈':['燈','霧燈','方向燈'],
        '停車':['違停','停','車'],'違停':['違停','停','車'],
        '雙白線':['雙白線','禁止變換車道線'],'禁止變換車道線':['雙白線','禁止變換車道線'],
        '並排':['並排','併排'],'併排':['並排','併排'],
        '橋梁':['橋梁','橋樑'],'橋樑':['橋梁','橋樑'],
        '三十五條':['酒'],
        '邊線':list('路面邊線'),
        '記錄':['記錄','紀錄'],'紀錄':['記錄','紀錄'],
        '聯結車':['聯結車','大客車','大貨車','大型車'],'大客車':['聯結車','大客車','大貨車','大型車'],'大貨車':['聯結車','大客車','大貨車','大型車'],'大型車':['聯結車','大客車','大貨車','大型車'],
        '慢車':['電動自行車','電動輔助自行車','慢車'],'電動自行車':['電動自行車','慢車'],'電動輔助自行車':['電動輔助自行車','慢車'],
        '次':['累','次'],'累':['累','次'],
        '轉彎':list('左轉彎')+list('右轉彎'),
        '交通事故':list("交通事故肇事"),
        '食':list("食飲"),
        '轉彎不依標誌、標線、號誌指示':list("轉彎兩段式"),
        '越級':list('領有，駕駛'),
        '不服':list("拒絕"),
        '乘':list("乘客")
        }
    all_list = word_list + list(symWords.keys())
    Contents_list = []
    msg_d2 = setstring(msg,all_list)
    msg_D1 = D2toD1(msg_d2,symWords)
    for i in data["Contents"]:   
        Contents_list.append(setstring(i,all_list))
    for i in Contents_list :
        Contents_list[Contents_list.index(i)] = D2toD1(i,symWords)
    filt = []
    result = []
    for i in range(0,len(Contents_list)):
        if set(msg_D1).issubset(set(Contents_list[i])):
            result.append(TextComponent(text=data.index[i],align="center",size="xl",weight="bold",color='#4260f5'))
            result.append(TextComponent(text=data["Contents"][i],size="lg",wrap = True))
            result.append(TextComponent(text="處罰：",size="lg",weight="bold",color="#f54242"))
            result.append(TextComponent(text=data["Punishment"][i],size="lg",wrap = True))
            result.append(TextComponent(text="註記：",size="lg",weight="bold",color="#27d10d"))
            result.append(TextComponent(text=data["Remark"][i],size="lg",wrap = True))
            result.append(SeparatorComponent(color='#0000FF'))
    reply.contents.body.contents = result
    if len(result) >= 300:
        reply = FlexSendMessage(
            alt_text='內容太多了',
            contents=BubbleContainer(
                size="giga",
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                    TextComponent(text="內容太多了，請增加關鍵字以利縮小範圍喔！",align="center",size="xl",weight="bold",color='#4260f5')
                    ]
                    )
                )
            )
    return reply
def getFlexbyNos(Nos):
    keys = Nos.split(",")
    a = keys[0].replace(" ","")
    try:
        p = keys[1].replace(" ","")
    except IndexError:
        p = ""
    try:
        s = keys[2].replace(" ","")
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
    reply = FlexSendMessage(
        alt_text='條號搜尋結果',
        contents=BubbleContainer(
            size="giga",
            body=BoxComponent(
                layout='vertical',
                contents=[]
                    )
            )
        )
    result_df = df.loc[result]
    content = []
    for i in range(0,len(result_df)):
        content.append(TextComponent(text=result_df.index[i],align="center",size="xl",weight="bold",color='#4260f5'))
        content.append(TextComponent(text=result_df["Contents"][i],size="lg",wrap = True))
        content.append(TextComponent(text="處罰：",size="lg",weight="bold",color="#f54242"))
        content.append(TextComponent(text=result_df["Punishment"][i],size="lg",wrap = True))
        content.append(TextComponent(text="註記：",size="lg",weight="bold",color="#27d10d"))
        content.append(TextComponent(text=result_df["Remark"][i],size="lg",wrap = True))
        content.append(SeparatorComponent(color='#0000FF'))
    reply.contents.body.contents = content
    return reply
import pandas as pd
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
# msg = "酒駕"
# if "酒駕" in msg :
#     msg = msg.replace("酒駕"," ")
#     result = NosFiltWords("35",msg)
# print(result)
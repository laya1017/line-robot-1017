import pandas as pd
df = pd.read_csv("data.csv")
df.set_index("Nos",inplace = True)
def Nos_finder():
    A = df.index
    ar = []
    item = []
    sub = []
    result = []
    remove_repaet = []
    for i in A:
        art = str(input("輸入條：")) + "條"
        for j in A:
            if len(art) == len(j[:j.index("條") + 1]) and art in j:
                ar.append(j)
        break
    for i in ar :
        if "項" in i:
            q = str(input("輸入項：")) + "項"
            for j in ar:
                if q in j :
                    item.append(j)
            for k in item:
                if "款" in k:
                    b = str(input("輸入款：")) + "款"
                    for l in item:
                        try:
                            if len(b) == len(l[l.index("項") + 1:l.index("款") + 1]) and b in l:
                                sub.append(l)
                        except ValueError:
                            sub = []
                    break
                break # j的迴圈
        elif "款" in i and "項" not in i:
            b = str(input("輸入款：")) + "款"
            for j in ar:
                try:
                    if len(b) == len(j[j.index("條") + 1: j.index("款")+ 1]) and b in j :
                        sub.append(j)
                except ValueError:
                    sub = []
                    
        break # i的迴圈
    if sub == [] and item != []:
        result = item
    elif sub != [] and item != []:
        result = sub
    elif sub == [] and item == []:
        result = ar
    elif sub != [] and item == []:
        result = sub
    elif ar == []:
        result = "找不到，如尋找更細部法規請至全國法規網查詢。"
    for i in result:
        if i not in remove_repaet:
            remove_repaet.append(i)
    final = []
    for i in remove_repaet:
        if str(type(df.loc[i])) == "<class 'pandas.core.frame.DataFrame'>" :
            for j in range(0,len(df.loc[i])):
                final.append(i +"：\n" + df.loc[i]["Contents"][j] + "\n處罰：" + df.loc[i]["Punishment"][j].strip("\n") + "\n註記：\n" + df.loc[i]["Remark"][j] + "\n")
        else:
            final.append(i +"：\n"+df.loc[i]["Contents"] + "\n處罰：" + df.loc[i]["Punishment"].strip("\n") + "\n註記：\n" + df.loc[i]["Remark"]+ "\n")
    return "".join(final).strip("\n")
def Content_finder(words):
    cdf = df
    keys = words.split(" ")
    for key in keys :
        condition = cdf["Contents"].str.contains(key)
        cdf = cdf[condition]
    result = []
    for i in range(0,len(cdf)):
        result.append(cdf.index[i] + "：\n" + cdf['Contents'][i] +
             "\n處罰：" + cdf["Punishment"][i].strip("\n") + "\n註記：\n" + cdf["Remark"][i] + "\n")
    return "".join(result).strip("\n")
# select = str(input("1.以法條查詢\n2.以內容查詢\n請輸入："))
# while select == "1" or "2":
#     if select == "1":
#         print(Nos_finder())
#     elif select == "2":
#         print(Content_finder())
#     select = str(input("1.以法條查詢\n2.以內容查詢\n請輸入："))




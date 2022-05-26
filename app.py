from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, render_template,g
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
import datetime
import search
import csv
import gspread
import requests
import redis
app = Flask(__name__)
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
            QuickReplyButton(action=MessageAction(label="駕照 吊扣", text="駕照 吊扣")),
            QuickReplyButton(action=MessageAction(label="牌照 吊銷", text="牌照 吊銷")),
            QuickReplyButton(action=MessageAction(label="牌照 吊扣", text="牌照 吊扣")),
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
                text='戶籍地、駕籍地、行為地？',
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
                ),
            CarouselColumn(
                title='未滿14歲違規人填單須知',
                text='本人？代理人？',
                actions=[
                    MessageAction(
                        label='按我',
                        text='未滿14歲之人填單規定'
                        )
                ]
                ),
            CarouselColumn(
                title='民眾檢舉交通違規新修規定',
                text='111.4.30開始施行',
                actions=[
                    MessageAction(
                        label='按我',
                        text='民眾檢舉交通違規新修規定'
                        )
                ]
                )
                ]
            )
        )
    return QA
def selects_nos_mode_P(event,uid,Nos):
    reply = TemplateSendMessage(alt_text="第"+Nos+"條第＿項？",
        template=ButtonsTemplate(
            title="第"+Nos+"條第＿項？",
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
    reply = TemplateSendMessage(alt_text="第"+Nos+"條第＿款？",
        template=ButtonsTemplate(
            title="第"+Nos+"條第＿款？",
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
    reply = TemplateSendMessage(alt_text="第"+Nos+"條第"+NosP+"項第＿款？",
        template=ButtonsTemplate(
            title="第"+Nos+"條第"+NosP+"項第＿款？",
            text='若要繼續查詢則直接輸入',
            actions=[
                MessageAction(
                    label="第"+Nos+"條第"+NosP+"項的所有法條",
                    text="第"+Nos+"條第"+NosP+"項的所有法條"
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
def Sort_Mode(event):
    reply = TemplateSendMessage(alt_text="條號搜尋模式。\n請輸入條號(第＿條)：",
        template=ButtonsTemplate(
            title="違規分類模式",
            text='選擇如下：',
            actions=[
                MessageAction(
                    label="汽機車",
                    text="CarsNscooter"
                    ),
                MessageAction(
                    label="慢車",
                    text="SMV"
                    ),
                MessageAction(
                    label="行人",
                    text="Pedestrian"
                    ),
                MessageAction(
                    label="道路障礙",
                    text="RoadObstacles"
                    )
            ]
        ))
    return reply
flex = {
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "size": "kilo",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "汽機車應到案處所檢核",
                "size": "xl",
                "wrap": True
              }
            ],
            "margin": "xxl"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "一.肇事致⼈傷亡\n二.抗拒稽查致傷害\n三.駕駛⼈或乘客無照且無法查明其⼾籍所在地\n四.汽⾞買賣業或汽⾞修理業違反本條例第57條規定。\n五.違反35條規定",
                    "wrap": True
                  }
                ]
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "符合以上五項之一",
                  "text": "符合以上五項之一"
                },
                "color": "#00DB00",
                "style": "primary",
                "height": "sm"
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "以上皆非(下一步)",
                  "text": "以上皆非(下一步)"
                },
                "style": "secondary",
                "color": "#EA0000",
                "height": "sm",
                "margin": "none"
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "離開",
                  "text": "Exit"
                },
                "height": "sm"
              }
            ]
          }
        },
        {
          "type": "bubble",
          "size": "kilo",
          "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "汽機車應到案處所檢核\n(執業登記證)",
                "size": "xl",
                "wrap": True
              }
            ]
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": "計程⾞駕駛⼈違反36、37條應受吊扣或廢⽌執業登記證",
                        "wrap": True,
                        "size": "lg",
                        "margin": "sm",
                        "align": "start"
                      }
                    ]
                  }
                ]
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "符合以上二項之一",
                  "text": "符合以上二項之一"
                },
                "color": "#00DB00",
                "style": "primary",
                "height": "sm"
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "以上皆非(回上一步)",
                  "text": "以上皆非(回上一步)"
                },
                "style": "secondary",
                "color": "#EA0000",
                "height": "sm"
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "離開",
                  "text": "Exit"
                },
                "height": "sm"
              }
            ]
          }
        }
      ]
    }
noResult = {
      "type": "bubble",
      "size": "giga",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "本系統以裁罰基準表內容為主，如查不到法條請上全國法規網。",
            "weight": "bold",
            "size": "xxl",
            "margin": "none",
            "align": "center",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "baseline",
            "margin": "none",
            "contents": [
              {
                "type": "text",
                "text": "可點擊下列交通相關法規尋找",
                "size": "xl",
                "color": "#eb4034",
                "margin": "none",
                "wrap": True,
                "weight": "bold"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "一、",
                    "flex": 1,
                    "size": "lg"
                  },
                  {
                    "type": "text",
                    "wrap": True,
                    "size": "lg",
                    "flex": 6,
                    "margin": "none",
                    "contents": [
                      {
                        "type": "span",
                        "text": "道路交通管理處罰條例",
                        "color": "#0335fc",
                        "weight": "bold"
                      },
                      {
                        "type": "span",
                        "text": "搜尋頁面"
                      }
                    ]
                  }
                ],
                "action": {
                  "type": "uri",
                  "label": "道交條例",
                  "uri": "https://liff.line.me/1657051965-j3lD0abP"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "二、",
                        "flex": 1,
                        "size": "lg"
                      },
                      {
                        "type": "text",
                        "text": "違反道路交通管理事件統一裁罰基準及處理細則搜尋頁面",
                        "wrap": True,
                        "size": "lg",
                        "flex": 6,
                        "margin": "none",
                        "contents": [
                          {
                            "type": "span",
                            "text": "違反道路交通管理事件統一裁罰基準及處理細則",
                            "color": "#0335fc",
                            "weight": "bold"
                          },
                          {
                            "type": "span",
                            "text": "搜尋頁面"
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                          {
                            "type": "text",
                            "text": "三、",
                            "flex": 1,
                            "size": "lg"
                          },
                          {
                            "type": "text",
                            "wrap": True,
                            "size": "lg",
                            "flex": 6,
                            "margin": "none",
                            "contents": [
                              {
                                "type": "span",
                                "text": "道路交通安全規則",
                                "color": "#0335fc",
                                "weight": "bold"
                              },
                              {
                                "type": "span",
                                "text": "搜尋頁面"
                              }
                            ]
                          }
                        ]
                      }
                    ],
                    "action": {
                      "type": "uri",
                      "label": "道安規則",
                      "uri": "https://liff.line.me/1657051965-X5YR8Ere"
                    }
                  }
                ],
                "action": {
                  "type": "uri",
                  "label": "處理細則",
                  "uri": "https://liff.line.me/1657051965-GZbp43YJ"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "四、",
                        "flex": 1,
                        "size": "lg"
                      },
                      {
                        "type": "text",
                        "wrap": True,
                        "size": "lg",
                        "flex": 6,
                        "margin": "none",
                        "contents": [
                          {
                            "type": "span",
                            "text": "道路交通標誌標線號誌設置規則",
                            "color": "#0335fc",
                            "weight": "bold"
                          },
                          {
                            "type": "span",
                            "text": "搜尋頁面"
                          }
                        ]
                      }
                    ]
                  }
                ],
                "action": {
                  "type": "uri",
                  "label": "設置規則",
                  "uri": "https://liff.line.me/1657051965-Jn6yjwgm"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "五、",
                        "flex": 1,
                        "size": "lg"
                      },
                      {
                        "type": "text",
                        "text": "有無攜帶凶器或其他危險物品？\n(加重要件)",
                        "wrap": True,
                        "size": "lg",
                        "flex": 6,
                        "margin": "none",
                        "contents": [
                          {
                            "type": "span",
                            "text": " 高速公路及快速公路管制規則",
                            "color": "#0335fc",
                            "weight": "bold"
                          },
                          {
                            "type": "span",
                            "text": "搜尋頁面"
                          }
                        ]
                      }
                    ]
                  }
                ],
                "action": {
                  "type": "uri",
                  "label": "高管規則",
                  "uri": "https://liff.line.me/1657051965-RZNxa6Vd"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "spacing": "sm",
                    "contents": [
                      {
                        "type": "text",
                        "text": "六、",
                        "flex": 1,
                        "size": "lg"
                      },
                      {
                        "type": "text",
                        "text": "有無攜帶凶器或其他危險物品？\n(加重要件)",
                        "wrap": True,
                        "size": "lg",
                        "flex": 6,
                        "margin": "none",
                        "contents": [
                          {
                            "type": "span",
                            "text": "行政令函",
                            "color": "#0335fc",
                            "weight": "bold"
                          },
                          {
                            "type": "span",
                            "text": "搜尋頁面"
                          }
                        ]
                      }
                    ]
                  }
                ],
                "action": {
                  "type": "uri",
                  "label": "行政令函",
                  "uri": "https://liff.line.me/1657051965-aB0XY34n"
                }
              }
            ]
          }
        ]
      }
    }
#Add User Method
def unit_row(userData):
    try:
        return int(str(sh.findall(userData[2])[-1]).split(" ")[1][1:-2])
    except:
        return False
def Series_Q_Reply(reply):
    DoubleYellow = QuickReply(items=[QuickReplyButton(action=MessageAction(label="雙黃線左轉問題",text="DoubleYellow"))])
    DoubleWhite = QuickReply(items=[QuickReplyButton(action=MessageAction(label="跨越雙白線問題",text="DoubleWhite"))])
    OtherLaw = QuickReply(items=[QuickReplyButton(action=MessageAction(label="60-2-3使用時機",text="OtherLaw"))])
    ThreeMinutes = QuickReply(items=[QuickReplyButton(action=MessageAction(label="3分鐘問題",text="ThreeMinutes"))])
    TwoCarStoppingNparking = QuickReply(items=[QuickReplyButton(action=MessageAction(label="併排停車認定標準",text="TwoCarStoppingNparking"))])
    StoppingPersuasion = QuickReply(items=[QuickReplyButton(action=MessageAction(label="臨時停車勸導要件",text="StoppingPersuasion"))])
    ParkingPersuasion = QuickReply(items=[QuickReplyButton(action=MessageAction(label="違規停車勸導要件",text="ParkingPersuasion"))])
    KeepIssueParking = QuickReply(items=[QuickReplyButton(action=MessageAction(label="停車連續舉發條件",text="KeepIssueParking"))])
    KeepIssueParking2 = QuickReply(items=[QuickReplyButton(action=MessageAction(label="停車連續\"逕\"舉條件",text="KeepIssueParking2"))])
    KeepIssueSpeed = QuickReply(items=[QuickReplyButton(action=MessageAction(label="超速連續\"逕\"舉條件",text="KeepIssueSpeed"))])
    OverWeightrange = QuickReply(items=[QuickReplyButton(action=MessageAction(label="超重勸導範圍",text="OverWeightrange"))])
    Warning52 = QuickReply(items=[QuickReplyButton(action=MessageAction(label="取締超速位置條件",text="Warning52"))])
    SideStopping = QuickReply(items=[QuickReplyButton(action=MessageAction(label="臨時停車路緣距離",text="SideStopping"))])
    SideParking = QuickReply(items=[QuickReplyButton(action=MessageAction(label="停車路緣距離",text="SideParking"))])
    LightUsing = QuickReply(items=[QuickReplyButton(action=MessageAction(label="燈光使用規定",text="LightUsing"))])
    HMOT = QuickReply(items=[QuickReplyButton(action=MessageAction(label="大重機上高速公路條件",text="HMOT"))])
    Machine = QuickReply(items=[QuickReplyButton(action=MessageAction(label="動力機械駕照條件",text="Machine"))])
    wrongWayDriving = QuickReply(items=[QuickReplyButton(action=MessageAction(label="來車道？遵行方向？",text="wrongWayDriving"))])
    FaultSign = QuickReply(items=[QuickReplyButton(action=MessageAction(label="故障標誌距離",text="FaultSign"))])
    CrashSign = QuickReply(items=[QuickReplyButton(action=MessageAction(label="故障標誌距離(肇事)",text="CrashSign"))])
    ProhibitDriver = QuickReply(items=[QuickReplyButton(action=MessageAction(label="禁止行駛之效果",text="ProhibitPassDrive"))])
    ProhibitPass = QuickReply(items=[QuickReplyButton(action=MessageAction(label="禁止通行之效果",text="ProhibitPassDrive"))])
    ProhibitDriveCar = QuickReply(items=[QuickReplyButton(action=MessageAction(label="禁止行駛之效果",text="ProhibitPassDrive"))])
    MakeCorrections = QuickReply(items=[QuickReplyButton(action=MessageAction(label="\"責令\"之填單處理",text="MakeCorrections"))])
    reply = QuickReplySet(reply,Machine,"21條")
    reply = QuickReplySet(reply,HMOT,"21條")
    reply = QuickReplySet(reply,OverWeightrange,"29-2條1項")
    reply = QuickReplySet(reply,OverWeightrange,"29-2條2項")
    reply = QuickReplySet(reply,Machine,"32條1項")
    reply = QuickReplySet(reply,KeepIssueSpeed,"40條")
    reply = QuickReplySet(reply,Warning52,"40條")
    reply = QuickReplySet(reply,LightUsing,"42條")
    reply = QuickReplySet(reply,DoubleWhite,"45條")
    reply = QuickReplySet(reply,wrongWayDriving,"45條1項1款")
    reply = QuickReplySet(reply,wrongWayDriving,"45條1項3款")
    reply = QuickReplySet(reply,DoubleYellow,"48條")
    reply = QuickReplySet(reply,DoubleYellow,"49條")
    reply = QuickReplySet(reply,StoppingPersuasion,"55條")
    reply = QuickReplySet(reply,ParkingPersuasion,"56條")
    reply = QuickReplySet(reply,ThreeMinutes,"55條")
    reply = QuickReplySet(reply,SideStopping,"55條")
    reply = QuickReplySet(reply,TwoCarStoppingNparking,"55條4款")
    reply = QuickReplySet(reply,KeepIssueParking,"56條")
    reply = QuickReplySet(reply,ThreeMinutes,"56條")
    reply = QuickReplySet(reply,SideParking,"56條")
    reply = QuickReplySet(reply,KeepIssueParking2,"56條1項")
    reply = QuickReplySet(reply,KeepIssueParking2,"56條2項")
    reply = QuickReplySet(reply,TwoCarStoppingNparking,"56條2項")
    reply = QuickReplySet(reply,KeepIssueParking,"57條")
    reply = QuickReplySet(reply,KeepIssueParking2,"57條")
    reply = QuickReplySet(reply,FaultSign,"59條")
    reply = QuickReplySet(reply,OtherLaw,"60條2項3款")
    reply = QuickReplySet(reply,CrashSign,"依規定處置")
    reply = QuickReplySet(reply,ProhibitDriveCar,"禁止其行駛")
    reply = QuickReplySet(reply,ProhibitDriver,"禁止駕駛")
    reply = QuickReplySet(reply,ProhibitDriver,"禁止其駕駛")
    reply = QuickReplySet(reply,ProhibitPass,"禁止其通行")
    reply = QuickReplySet(reply,ProhibitPass,"禁止通行")
    reply = QuickReplySet(reply,MakeCorrections,"責令")
    return reply
def QuickReplySet(reply,condition,Nos):
    text = ""
    for i in range(0,len(reply.contents.body.contents),5):
        try:
            target += reply.contents.body.contents[i].text
        except:
            pass
    news = []
    if Nos in target:
        if reply.quick_reply == None:
            reply.quick_reply = condition
            return reply
        else:
            reply.quick_reply.items += condition.items
            for i in reply.quick_reply.items:
                if i not in news:
                    news.append(i)
        reply.quick_reply.items = news
        return reply
    else:
        return reply
def target(event):
    reply = TemplateSendMessage(alt_text="汽機車應到案處所檢核(處罰對象)",
        template=ButtonsTemplate(
            title="汽機車應到案處所檢核(處罰對象)",
            text='選擇如下：',
            actions=[
                MessageAction(
                    label="所有人",
                    text="Owner"
                    ),
                MessageAction(
                    label="駕駛人、乘客",
                    text="driverNpassenger"
                    ),
                MessageAction(
                    label="上一步",
                    text="Back to CheckCarsNscooter"
                    ),
                MessageAction(
                    label="離開",
                    text="Exit"
                    )
            ]
        ))
    return reply
def driverNpassengercheck(event):
    reply = TemplateSendMessage(alt_text="汽機車應到案處所檢核(駕駛人、乘客)",
        template=ButtonsTemplate(
            title="駕駛人或乘客有無持有駕駛執照？",
            text='選擇如下：',
            actions=[
                MessageAction(
                    label="有駕駛執照",
                    text="Have Driver License"
                    ),
                MessageAction(
                    label="無駕駛執照",
                    text="No Driver License"
                    ),
                MessageAction(
                    label="上一步",
                    text="Back to target"
                    ),
                MessageAction(
                    label="離開",
                    text="Exit"
                    )
            ]
        ))
    return reply
##Columns
def speedToRichMnu(msg):
    if msg == "[關鍵字搜尋模式]":
        keep_state(uid,"txt_mode")
        reply = enter_txt_mode(event)
    elif msg == "[條號搜尋模式]":
        keep_state(uid,"nos_mode")
        reply = enter_txt_mode(event)
    elif msg == "[[酒(毒)駕專區]]":
        keep_state(uid,"dwiNdwdenterButtons")
        reply = enter_txt_mode(event)    
    elif msg == " [[應到案日期計算]]":
        today = datetime.datetime.now()
        initialdate = str(today.year - 1911)+'-'+str(today.month)+'-'+str(today.day)
        expiryDate = today+datetime.timedelta(days = 30)
        finalDate = str(expiryDate.year - 1911)+'-'+str(expiryDate.month)+'-'+str(expiryDate.day)
        reply = TextSendMessage(text="今天日期為：\n"+initialdate+"\n應到案日期為：\n"+finalDate+"\n(當場舉發)")
        delete_data(uid)
        reply = enter_txt_mode(event)
    elif msg == "[[其他交通問題]]":
        keep_state(uid,"QnA")
        reply = enter_txt_mode(event)
    return reply
##dwiNdwd zone
def dwiNdwdbuttonFilt(msg):
    quick_reply=QuickReply(
        items=[
        QuickReplyButton(action=MessageAction(label="汽機車酒駕拒測告知", text="汽機車酒駕拒測告知")),
        QuickReplyButton(action=MessageAction(label="提審法", text="提審法")),
        QuickReplyButton(action=MessageAction(label="三項權利(刑訴95條)", text="三項權利(刑訴95條)")),
        QuickReplyButton(action=MessageAction(label="汽機車酒駕法條", text="汽機車酒駕法條")),
        QuickReplyButton(action=MessageAction(label="汽機車毒駕法條", text="汽機車毒駕法條")),
        QuickReplyButton(action=MessageAction(label="累犯法條", text="累犯法條")),
        QuickReplyButton(action=MessageAction(label="汽機車酒駕拒測法條", text="汽機車酒駕拒測法條")),
        QuickReplyButton(action=MessageAction(label="拒測累犯法條", text="拒測累犯法條")),
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
            text='懶得找可以按下方快速鈕',
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
        text = "1.慢車於道路交通管理處罰條例第73條2項及3項皆處罰為「\"酒精\"濃度超標」及「拒絕\"酒精\"濃度測試」，且於同法中並\"無\"規定服用藥物駕駛之處罰。\n2.但經尿液或血液中檢測有\"毒品、迷幻藥、麻醉藥品及其相類似之管制藥品\"成分時，則屬於刑法185-3條第1項「服用毒品、麻醉藥品或其他相類之物，致不能安全駕駛」，此情況建議將行為人(駕駛人)精神狀況以攝影器材紀錄，如可製作觀測表之情況則更好。",
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
def HabeasCorpusAct(event):
    reply = FlexSendMessage(
        alt_text='提審法',
        contents=BubbleContainer(
            size="giga",
            body=BoxComponent(
                layout='vertical',
                contents=[
                TextComponent(text="提審法§1",align="center",size="xl",weight="bold",color="#eb4034"),
                TextComponent(text='第一項：',size="lg",weight="bold"),
                TextComponent(text='人民被法院以外之任何機關逮捕、拘禁時，其本人或他人得向逮捕、拘禁地之地方法院聲請提審。但其他法律規定得聲請即時由法院審查者，依其規定。',size="lg",wrap=True),
                TextComponent(text='第二項',size="lg",weight="bold"),
                TextComponent(text='前項聲請及第十條之抗告，免徵費用。',size="lg",wrap=True)
                ]
                )
            )
        )
    return reply
def CodeOfCriminalProcedure(event):
    reply = FlexSendMessage(
        alt_text='刑事訴訟法',
        contents=BubbleContainer(
            size="giga",body=BoxComponent(layout='vertical',contents=[
                BoxComponent(layout='vertical',contents=[
                    TextComponent(
                        text="三項權利(刑訴95條)",align="center",size="xl",weight="bold",color="#eb4034"),
                    TextComponent(
                        text="◯◯◯先生/小姐您涉嫌＿(罪名)＿，依法得行使下列權利：",size="lg",wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="一、",size="lg",flex=2,wrap=True),
                    TextComponent(
                        text="得保持緘默，無須違背自己之意思而為陳述。",size="lg",flex=8,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="二、",size="lg",flex=2,wrap=True),
                    TextComponent(
                        text="得選任辯護人。如為低收入戶、中低收入戶、原住民或其他依法令得請求法律扶助者，得請求之。",size="lg",flex=8,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="三、",size="lg",flex=2,wrap=True),
                    TextComponent(
                        text="得請求調查有利之證據。",size="lg",flex=8,wrap=True)]
                    )
                ]
                )
            )
        )
    return reply
def YouShouldWarn(event):
    reply = FlexSendMessage(
        alt_text='刑事訴訟法',
        contents=BubbleContainer(
            size="giga",body=BoxComponent(layout='vertical',contents=[
                BoxComponent(layout='vertical',contents=[
                    TextComponent(
                        text="⊙拒絕酒測告知事項：",align="center",size="xl",weight="bold",color="#eb4034"),
                    TextComponent(
                        text="一、初次違反：",size="lg",wrap=True,color="#a8329b")]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="1.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="罰鍰：新台幣18萬元",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="2.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="吊銷駕駛執照",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="3.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="應受道路交通安全講習",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="4.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="當場移置保管車輛",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="5.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="吊扣所駕車輛牌照2年",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="6.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="「如」租賃車業者已告知本條處罰規定，依所處罰鍰加重1/2。",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='vertical',contents=[
                    TextComponent(
                        text="二、「如」再次違反：",size="lg",wrap=True,color="#a8326b")]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="1.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="罰鍰：10年內第2次違反處新台幣36萬元，第3次以上按前次處罰加罰18萬元。",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="2.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="吊銷駕駛執照",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="3.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="應受道路交通安全講習",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="4.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="當場移置保管車輛",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="5.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="吊扣所駕車輛牌照2年",size="lg",flex=9,wrap=True)]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="6.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="公布姓名、照片及違法事情★",size="lg",flex=9,wrap=True,color="#db5a5a")]
                    ),
                BoxComponent(layout='baseline',contents=[
                    TextComponent(
                        text="7.",size="lg",flex=1,wrap=True),
                    TextComponent(
                        text="「如」租賃車業者已告知本條處罰規定，依所處罰鍰加重1/2。",size="lg",flex=9,wrap=True)]
                    )
                ]
                )
            )
        )
    return reply
##PlaceCheckMode
def PlaceCheckMode(event):
    reply = TemplateSendMessage(alt_text="應到案處所檢核系統",
        template=ButtonsTemplate(
            title="應到案處所檢核系統",
            text='選擇車種(慢車、行人、道路障礙)',
            actions=[
                MessageAction(
                    label="汽機車",
                    text="CarsNscooter"
                    ),
                MessageAction(
                    label="大眾捷運系統車輛",
                    text='MassRapidTransitSystemVehicles'
                    ),
                MessageAction(
                    label="慢車、行人、道路障礙",
                    text="SMV,PED,OBS"
                    ),
                MessageAction(
                    label="離開",
                    text='Exit'
                    )
            ]
        ))
    return reply
##SQL CMD
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hbisksmwaizgve:c13df8043f36aa6c9a985dca8d1d373c60d76453286bcc62f7055958fe799f4d@ec2-34-231-63-30.compute-1.amazonaws.com:5432/dc0ift2b69djpl"
db = SQLAlchemy(app)
def delete_data(uid):
    sql_cmd = "DELETE FROM userstate WHERE  uid ='"+uid+"'"
    db.engine.execute(sql_cmd)
def keep_state(uid, mode):
    sql_cmd = "INSERT INTO userstate (uid, state) values('"+uid+"','"+mode+"');"
    db.engine.execute(sql_cmd)
def change_state(uid, mode):
    sql_cmd = "UPDATE userstate SET state = '"+mode+"' WHERE uid = '"+uid+"'"
    db.engine.execute(sql_cmd)
def change_var(uid, var, msg):
    sql_cmd = "UPDATE userstate SET "+var+" = '"+msg+"' WHERE uid = '"+uid+"'"
    db.engine.execute(sql_cmd)   
def get_var(uid, var):
    sql_cmd = "SELECT "+var+" FROM userstate  WHERE uid = '"+uid+"'"
    return list(db.engine.execute(sql_cmd))[0][0]
##SQL CMD 
app.config['SESSION_REDIS'] = redis.Redis(host='redis-17410.c1.asia-northeast1-1.gce.cloud.redislabs.com', port='17410', password='ruV3jiVuCZqqVnZOp7CDOUIJDKuB5ViN')
r = app.config['SESSION_REDIS']
# 增加全局变量g.stk_num
gc = gspread.service_account(filename = "vigilant-tract-350212-a22f69b7e842.json")
managers_id = gc.open("user_id").get_worksheet(1).col_values(1)
sh = gc.open("user_id").sheet1
users_list = sh.get_all_values()
ID_list = sh.col_values(2)
count_units = sh.col_values(3)
units = []
cacus = []
count_units_sh = []
for i in users_list:
  if i[2] not in units:
    units.append(i[2])
for i in count_units:
    if "溪湖" in i :
        count_units_sh.append(i)
cacus.append("溪湖分局共"+str(len(count_units_sh))+"人登錄")
for i in units:
    count = 1
    cacus.append(i+"("+str(count_units.count(i))+"人登錄)"+"登錄成員有：")
    for j in users_list:
        if j[2] == i:
            cacus.append(str(count)+"."+j[0])
            count += 1
r.set('managers_id',",".join(managers_id))
r.set('ID_list',",".join(ID_list))
r.set('cacus',"\n".join(cacus))
@app.route("/")
def index():
    return render_template("index.html")
line_bot_api = LineBotApi('m2UPwMSn3p4xmDvVQkvo+AFGkZONQ0yKm3vQlm/RKMODbcTLoEPhS3oQNsqmWciOl3+hxaSy1LrUGQAJ0AxbaS2yTchTCy7Ux5gsMQmsUYkQSO27KIeDhR78RcekWmeF/zvvuMsmudmHMc0OdukCuQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('aa64bf9da34389763d2020a499d6d6ec')
@app.route("/Delete_datas")
def Delete_datas():
    sql_cmd = "TRUNCATE TABLE userstate"
    db.engine.execute(sql_cmd)   
    return "刪除成功"
@app.route("/Update")
def Update():
    gc = gspread.service_account(filename = "vigilant-tract-350212-a22f69b7e842.json")
    managers_id = gc.open("user_id").get_worksheet(1).col_values(1)
    sh = gc.open("user_id").sheet1
    users_list = sh.get_all_values()
    ID_list = sh.col_values(2)
    count_units = sh.col_values(3)
    units = []
    cacus = []
    count_units_sh = []
    for i in users_list:
      if i[2] not in units:
        units.append(i[2])
    for i in count_units:
        if "溪湖" in i :
            count_units_sh.append(i)
    cacus.append("溪湖分局共"+str(len(count_units_sh))+"人登錄")
    for i in units:
        count = 1
        cacus.append(i+"("+str(count_units.count(i))+"人登錄)"+"登錄成員有：")
        for j in users_list:
            if j[2] == i:
                cacus.append(str(count)+"."+j[0])
                count += 1
    # r.set('gc',str(gc))
    r.set('managers_id',",".join(managers_id))
    r.set('ID_list',",".join(ID_list))
    r.set('cacus',"\n".join(cacus))
    return "更新成功"
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: "+body)
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
    sql_cmd = "SELECT * from userstate where uid ='"+uid+"'"
    uid_data = db.engine.execute(sql_cmd)
    user_name = line_bot_api.get_profile(uid).display_name
    datalist = list(uid_data)
    if uid not in r.get("ID_list").decode('utf-8').split(',') :
        if  msg == "告訴我ID":
            reply = TextSendMessage(text=(user_name +","+ uid))
        else:
            reply = TextSendMessage(text="抱歉，您並非認證之成員，請洽管理員登記，謝謝。")
    elif msg == "Machine":
        reply = TextSendMessage(text="道安規則§83-2：\n動力機械行駛於道路時，其駕駛人必須領有小型車以上之駕駛執照。但自中華民國96年1月1日起，總重量逾3.5公噸之動力機械，其駕駛人應領有大貨車以上之駕駛執照；自中華民國101年1月1日起，重型及大型重型之動力機械，其駕駛人應領有聯結車駕駛執照。")
    elif msg == "HMOT":
        reply = TextSendMessage(text="道交條例§92II：\n汽缸排氣量550立方公分以上大型重型機車，得依交通部公告規定之路段及時段行駛高速公路，其駕駛人應有得駕駛汽缸排氣量550立方公分以上大型重型機車駕駛執照1年以上及小型車以上之駕駛執照。")
    elif msg == "LightUsing":
        reply = TextSendMessage(text="道安規則§102,I:\n右轉彎時，應距交岔路口30公尺前顯示方向燈或手勢，換入外側車道、右轉車道或慢車道，駛至路口後再行右轉。但由慢車道右轉彎時應於距交岔路口30至60公尺處，換入慢車道。\n五、左轉彎時，應距交岔路口30公尺前顯示方向燈或手勢，換入內側車道或左轉車道，行至交岔路口中心處左轉，並不得占用來車道搶先左轉。\n道安規則§109:\nI.汽車行駛時，應依下列規定使用燈光：\n  1.夜間應開亮頭燈。\n  2.行經隧道、調撥車道應開亮頭燈。\n  3.遇濃霧、雨、雪、天色昏暗或視線不清時，應開亮頭燈。\n  4.非遇雨、霧時，不得使用霧燈。\n  5.行經公路主管機關或警察機關公告之山區或特殊路線之路段，涵洞或車行地下道，應依標誌指示使用燈光。\n  6.夜間會車時，或同向前方100公尺內有車輛行駛，除第101條第3款之情形外，應使用近光燈。\nII.汽車駕駛人，應依下列規定使用方向燈：\n  1.起駛前應顯示方向燈。\n  2.左（右）轉彎時，應先顯示車輛前後之左（右）邊方向燈光；變換車道時，應先顯示欲變換車道方向之燈光，並應顯示至完成轉彎或變換車道之行為。\n  3.超越同一車道之前車時應顯示左方向燈並至與前車左側保持半公尺以上之間隔超過，行至安全距離後，再顯示右方向燈駛入原行路線。")
    elif msg == "DoubleYellow":
        reply = TextSendMessage(text="交通部94.06.15.交路字第0940035842號函：\n查道路交通管理處罰條例第48條應係對汽車駕駛人行駛至轉彎路段未依規定轉彎之處罰，對於本案臺中縣警察局所提汽車於繪有行車分向限制線段左轉彎，應係未依分向限制線標線規定行駛之違規轉彎行為，此與上述第48條之未依規定轉彎情形，應屬有間，本部同意貴署所提適用處罰條例第60條第2項第3款「不遵守道路交通標線之指示」之處罰。")
    elif msg == "DoubleWhite":
        reply = TextSendMessage(text="交通部99.07.26.交路字第0990044737號函：\n有關貴署函詢「跨越雙白線變換車道」違規案件之處罰疑義乙案，本部前業以75年8月18日交路(75)字第19567號函示「應依道路交通管理處罰條例第45條第1項第12款裁處」在案，復請查照。")
    elif msg == "ThreeMinutes":
        reply = TextSendMessage(text="依據立法院1010508修正理由：\n同時臨時停車之重點實則在於保持可立即行駛之狀態，不應以引擎是否熄火或停止時間來判斷")
    elif msg == "SideStopping":
        reply = TextSendMessage(text="道安規則§111 II,III：\nII.汽車臨時停車時，應依車輛順行方向緊靠道路邊緣，其前後輪胎外側距離緣石或路面邊緣不得逾60公分。但大型車不得逾1公尺。\nIII. 大型重型機車及機車臨時停車時，應依車輛順行方向緊靠道路邊緣停放，其前輪或後輪外側距離緣石或路面邊緣不得逾40公分。")
    elif msg == "SideParking":
        reply = TextSendMessage(text="道安規則§112 II,III：\nII.汽車停車時應依車輛順行方向緊靠道路邊緣，其前後輪胎外側距離緣石或路面邊緣不得逾40公分。\nIII. 大型重型機車及機車停車時，應依車輛順行方向緊靠道路邊緣平行、垂直或斜向停放，其前輪或後輪外側距離緣石或路面邊緣不得逾30公分。但公路主管機關、市區道路主管機關或警察機關另有特別規定時，應依其規定。")
    elif msg == "OtherLaw":
        reply = TextSendMessage(text="道交條例60條2項3款使用時機在於交通違規找不到符合本法之行為以及違反\"禁制\"標誌或標線之情況下適用，故考路以本條款舉發時需多加詳查規定。")
    elif msg == "wrongWayDriving":
        reply = TextSendMessage(
            text="1.遵行方向：\n依據道路交通標誌標線號誌設置規則第2章第3節禁制標誌內容可知，係指道路上設具有方向性質之\"遵行\"標誌（藍底白色箭頭），例如：道路遵行方向、車道遵行方向標誌、單行道標誌等，而車輛必須\"遵行\"其標誌方向行駛。\n2.來車道：\n依據道安規則§97-1項2款規定「在劃有分向限制線之路段，不得駛入來車之車道內。」可得知，在劃有雙黃線之情況駛入來車道（對向車道），符合道交條例45條1項3款之違規行為。",
            quick_reply=QuickReply(
                items=[QuickReplyButton(action=MessageAction(label="遵行方向標誌圖形", text="complianceSign"))
                ]
                )
            )
    elif msg == "TwoCarStoppingNparking":
        reply = ImageSendMessage(
            original_content_url='https://raw.githubusercontent.com/laya1017/image/main/TwoCarStoppingNparking.jpg',
            preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/TwoCarStoppingNparking.jpg')
    elif msg == "OverWeightrange":
        reply = TextSendMessage(text="處理細則§12,I：\n駕駛汽車裝載貨物超過核定之總重量或總聯結重量，未逾10%得勸導。\n處理細則§12,II：\n行為人發生交通事故有前項規定行為，除本條例第14條第2項第3款、第25條第2項、第69條第2項或第71條之情形外，仍得舉發。\n處理細則§13,II：\n貨車超載應責令當場卸貨分裝，如無法當場卸貨分裝者，其超載重量未逾核定總重量20%者，責令其於2小時內改正之，逾2小時不改正者，得連續舉發；其超載重量逾核定總重量20%者，當場禁止其通行。")
    elif msg == "complianceSign":
        reply = ImageSendMessage(
            original_content_url='https://raw.githubusercontent.com/laya1017/image/main/complianceSign.jpg',
            preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/complianceSign.jpg')
    elif msg == "KeepIssueSpeed":
        reply = TextSendMessage(text="道交條例§85-1,II：\n(1)逕行舉發汽車行車速度超過規定之最高速限或低於規定之最低速度或有違反第33條第1項、第2項之情形，其違規地點相距6公里以上、違規時間相隔6分鐘以上或行駛經過一個路口以上得連續舉發。但其違規地點在隧道內者，不在此限。")
    elif msg == "KeepIssueParking2":
        reply = TextSendMessage(text="道交條例§85-1,II：\n二、逕行舉發汽車有第56條第1項、第2項或第57條規定之情形，而駕駛人、汽車所有人、汽車買賣業、汽車修理業不在場或未能將汽車移置每逾2小時得連續舉發。")
    elif msg == "KeepIssueParking":
        reply = TextSendMessage(text="道交條例§85-1,I：\n汽車駕駛人、汽車所有人、汽車買賣業或汽車修理業違反第56條第1項或第57條規定，經舉發後，不遵守交通勤務警察或依法令執行交通稽查任務人員責令改正者，得連續舉發之。")
    elif msg == "Warning52":
        reply = ImageSendMessage(
            original_content_url='https://raw.githubusercontent.com/laya1017/image/main/Warning52.png',
            preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/Warning52.png')
    elif msg == "StoppingPersuasion":
        reply = TextSendMessage(text="處理細則§12,I：\n駕駛汽車因上、下客、貨，致有本條例第55條之情形，惟尚無妨礙其他人、車通行。")
    elif msg == "ParkingPersuasion":
        reply = TextSendMessage(text="處理細則§12,I：\n深夜時段（0至6時）停車，有本條例第56條第1項之情形。但於身心障礙專用停車位違規停車或停車顯有妨礙消防安全之虞，或妨礙其他人車通行經人檢舉者，不在此限。")
    elif msg == "FaultSign":
        reply = TextSendMessage(text="道安規則§112,IV：\n(1)在行車時速40公里以下之路段，應豎立於車身後方5公尺至30公尺之路面上，車前適當位置得視需要設置。\n(2)在行車時速逾40公里之路段，應豎立於車身後方30公尺至100公尺之路面上，車前適當位置得視需要設置。\n(3)交通擁擠之路段，應懸掛於車身之後部，車前適當位置得視需要設置。")
    elif msg == "CrashSign":
        reply = TextSendMessage(text="道路交通事故處理辦法§4,I：\n1.高速公路：於事故地點後方100公尺處。\n2.快速道路或最高速限超過60公里之路段：於事故地點後方80公尺處。\n3.最高速限超過50公里至60公里之路段：於事故地點後方50公尺處。\n4.最高速限50公里以下之路段：於事故地點後方30公尺處。\n5.交通壅塞或行車時速低於10公里以下之路段：於事故地點後方5公尺處。\nII：\n前項各款情形，遇雨霧致視線不清時，適當距離應酌予增加；其有雙向或多向車流通過，應另於前方或周邊適當處所為必要之放置。")
    elif msg == "ProhibitPassDrive":
        reply = TextSendMessage(text="道交條例§85-2,I：\n車輛所有人或駕駛人依本條例規定應予禁止通行、禁止其行駛、禁止其駕駛者，交通勤務警察或依法令執行交通稽查任務人員應當場執行之，必要時，得逕行移置保管其車輛。\n處理細則§11,II：\n對於依規定須責令改正、禁止通行、禁止其行駛、禁止其駕駛者、補換牌照、駕照等事項，應當場告知該駕駛人或同車之汽車所有人，並於通知單記明其事項或事件情節及處理意見，供裁決參考。")
    elif msg == "MakeCorrections" :
        reply = TextSendMessage(text="處理細則§11,II：\n對於依規定須責令改正、禁止通行、禁止其行駛、禁止其駕駛者、補換牌照、駕照等事項，應當場告知該駕駛人或同車之汽車所有人，並於通知單記明其事項或事件情節及處理意見，供裁決參考。")
    elif uid in r.get("managers_id").decode('utf-8').split(',') and "sh-users" in msg:
        reply = TextSendMessage(text=r.get("cacus").decode('utf-8'))
    elif (uid in ["Uc0e274a2c86b4e44c9162859362614a9"] or uid in r.get("managers_id").decode('utf-8').split(',')) and "add-user" in msg:
        msg = msg.replace("add-user","").replace(" ","")
        userData = msg.split(",")
        try:
            realname = line_bot_api.get_profile(userData[1]).display_name
            if userData[1] not in (r.get("ID_list").decode('utf-8').split(',')):
                if unit_row(userData) == False:
                    sh.append_row(userData,unit_row(userData) + 1)
                else:
                    sh.insert_row(userData,unit_row(userData) + 1)
                requests.get("https://line-robot-1017.herokuapp.com/Update")
                reply = TextSendMessage(text="認證成功！")
            else:
                reply = TextSendMessage(text="此ID已經存在了！")
        except:
            reply = TextSendMessage(text="UserID無效。")
    elif (uid in ["Uc0e274a2c86b4e44c9162859362614a9"] or uid in r.get("managers_id").decode('utf-8').split(',')) and "del-user" in msg:
        msg = msg.replace("del-user","").replace(" ","")
        userData = msg.split(",")
        try:
            realname = line_bot_api.get_profile(userData[1]).display_name
            if userData[1] in (r.get("ID_list").decode('utf-8').split(',')):
                sh.delete_rows(unit_row(userData))
                requests.get("https://line-robot-1017.herokuapp.com/Update")
                reply = TextSendMessage(text=realname+"刪除了！")
            else:
              reply = TextSendMessage(text="不存在此使用者。")
        except:
            reply = TextSendMessage(text="此ID無效用")
    elif len(datalist) == 0:
        if msg == "[關鍵字搜尋模式]":
            keep_state(uid,"txt_mode")
            reply = enter_txt_mode(event)
        elif msg == "[分類查找模式]":
            keep_state(uid,"Sort_Mode")
            reply = Sort_Mode(event)
        elif msg == "[條號搜尋模式]" :
            keep_state(uid,"nos_mode")
            reply = enter_nos_mode(event)
        elif msg == "[[酒(毒)駕專區]]" :
            keep_state(uid,"dwiNdwdenterButtons")
            reply = dwiNdwdenterButtons(event,msg)
        elif msg == "[[應到案日期計算]]":
            today = datetime.datetime.now()
            initialdate = str(today.year - 1911)+'-'+str(today.month)+'-'+str(today.day)
            expiryDate = today+datetime.timedelta(days = 30)
            finalDate = str(expiryDate.year - 1911)+'-'+str(expiryDate.month)+'-'+str(expiryDate.day)
            reply = TextSendMessage(
                text="今天日期為：\n"+initialdate+"\n應到案日期為：\n"+finalDate+"\n(當場舉發)")
        elif msg == "[[新冠病毒防疫措施]]":
            reply = ImageSendMessage(
                original_content_url='https://raw.githubusercontent.com/laya1017/image/main/Covid.jpg',
                preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/Covid.jpg')
        elif msg == "[[其他交通問題]]":
            keep_state(uid,"QnA")
            reply = Other_QnA(event)
        else :
            reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
    elif len(datalist) != 0 :
        if  msg == "[關鍵字搜尋模式]":
            change_state(uid,"txt_mode")
            reply = enter_txt_mode(event)
        elif msg == "[分類查找模式]":
            change_state(uid,"Sort_Mode")
            reply = Sort_Mode(event)  
        elif msg == "[條號搜尋模式]" :
            change_state(uid,"nos_mode")
            reply = enter_nos_mode(event)
        elif msg == "[[酒(毒)駕專區]]" :
            change_state(uid,"dwiNdwdenterButtons")
            reply = dwiNdwdenterButtons(event,msg)
        elif msg == "[[應到案日期計算]]":
            today = datetime.datetime.now()
            initialdate = str(today.year - 1911)+'-'+str(today.month)+'-'+str(today.day)
            expiryDate = today+datetime.timedelta(days = 30)
            finalDate = str(expiryDate.year - 1911)+'-'+str(expiryDate.month)+'-'+str(expiryDate.day)
            reply = TextSendMessage(
                text="今天日期為：\n"+initialdate+"\n應到案日期為：\n"+finalDate+"\n(當場舉發)")
        elif msg == "[[新冠病毒防疫措施]]":
            reply = ImageSendMessage(
                original_content_url='https://raw.githubusercontent.com/laya1017/image/main/Covid.jpg',
                preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/Covid.jpg')
        elif msg == "[[其他交通問題]]":
            change_state(uid,"QnA")
            reply = Other_QnA(event)
        elif "reset" in msg :
            delete_data(uid)
            reply = TextSendMessage(text="重新啟動")
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
                reply = PlaceCheckMode(event)
                change_state(uid,"PlaceCheckMode")
            elif msg == "哪些違規不得郵繳？":
                reply = ImageSendMessage(
                    original_content_url='https://raw.githubusercontent.com/laya1017/image/main/postpay.png',
                    preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/postpay.png',
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to QnA")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "未滿14歲之人填單規定":
                reply = TextSendMessage(
                    text="1.未滿14歲之人違反本條例之規定，處罰其\"法定代理人\"或\"監護人\"(道交條例§85-4)。\n2.應於通知單上另行查填其法定代理人或監護人之：\n (1)姓名\n (2)身分證統一編號\n (3)地址\n (4)\"送達\"其\"法定代理人\"或\"監護人\"。(處理細則§11,I,3)",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="何謂法定代理人及監護人？", text="Guardians")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to QnA")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Guardians":
                reply = TextSendMessage(
                    text="<民法規定>\n●未成年人：未滿20歲(112年1月1日改為18歲)。\n●法定代理人：父母為其未成年子女之法定代理人。\n●監護人：\n 一.父母於一定期限內，以書面委託他人行使監護之職務。\n 二.對於未成年子女之權利、義務之父或母，得以遺囑指定監護人。\n 三.父或母，得以遺囑指定監護人。\n 四.父母均不能行使、負擔對於未成年子女之權利義務或父母死亡而無遺囑指定監護人，或遺囑指定之監護人拒絕就職時，依下列順序定其監護人(未能依下列順序定其監護人時，法院得依未成年子女、四親等內之親屬、檢察官、主管機關或其他利害關係人之聲請，為未成年子女之最佳利益，就其三親等旁系血親尊親屬、主管機關、社會福利機構或其他適當之人選定為監護人，並得指定監護之方法；如無下列之監護人，於法院依第三項為其選定確定前，由當地社會福利主管機關為其監護人。)：\n  1.與未成年人同居之祖父母。\n  2.與未成年人同居之兄姊。\n  3.不與未成年人同居之祖父母。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="未滿14歲之人填單規定")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "民眾檢舉交通違規新修規定":
                reply = ImageSendMessage(
                original_content_url='https://raw.githubusercontent.com/laya1017/image/main/S__21544962.jpg',
                preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/S__21544962.jpg',
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to QnA")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Back to QnA":
                reply = Other_QnA(event)
                change_state(uid, "QnA")
            else:
                reply = TextSendMessage(text="已跳出，請自選單重新開始。")
        elif datalist[0][2] == "PlaceCheckMode":
            if msg == "CarsNscooter":
                reply = FlexSendMessage(alt_text='汽機車應到案處所檢核',contents=flex)
                change_state(uid, "CheckCarsNscooter")
            elif msg == "MassRapidTransitSystemVehicles":
                reply = TextSendMessage(
                    text="大眾捷運系統車輛的應到案處所:\n營運機構監督機關所在地處罰機關",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to PlaceCheckMode")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "SMV,PED,OBS":
                reply = TextSendMessage(
                    text="慢車、行人、道路障礙的應到案處所:\n\"⾏為地警察機關\"",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to PlaceCheckMode")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Back to PlaceCheckMode":
                reply = PlaceCheckMode(event)
        elif datalist[0][2] == "CheckCarsNscooter":
            if msg == "符合以上五項之一":
                reply = TextSendMessage(
                    text="應到案處所為：\n\"行為地公路主管機關\"",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to CheckCarsNscooter")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        ))
            elif msg == "以上皆非(下一步)":
                reply = target(event)
                change_state(uid,"target")
            elif msg == "符合以上二項之一":
                reply = TextSendMessage(
                    text="應到案處所為：\n\"辦理執業登記之警察機關\"",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to CheckCarsNscooter")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        ))
            elif msg == "以上皆非(回上一步)":
                reply = PlaceCheckMode(event)
                change_state(uid, "PlaceCheckMode")
            elif msg == "Back to CheckCarsNscooter":
                reply = FlexSendMessage(alt_text='汽機車應到案處所檢核',contents=flex)
        elif datalist[0][2] == "target":
            if msg == "Owner":
                reply = TextSendMessage(
                    text="應到案處所為：\n\"車籍地公路主管機關\"",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to target")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        ))
            elif msg == "driverNpassenger":
                reply = driverNpassengercheck(event)
                change_state(uid, "dNpCheck")
            elif msg == "Back to target":
                reply = target(event)
            elif msg == "Back to CheckCarsNscooter":
                reply = FlexSendMessage(alt_text='汽機車應到案處所檢核',contents=flex)
                change_state(uid, "CheckCarsNscooter")
        elif datalist[0][2] == "dNpCheck":
            if msg == "Have Driver License":
                reply = TextSendMessage(
                    text="應到案處所為：\n\"駕籍地公路主管機關\"",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        ))
            elif msg == "No Driver License":
                reply = TextSendMessage(
                    text="應到案處所為：\n\"戶籍地公路主管機關\"",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        ))
            elif msg == "Back":
                reply = driverNpassengercheck(event)
            elif msg == "Back to target":
                reply = target(event)
                change_state(uid, "target")
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
                reply = search.getFlexbyNos(get_var(uid,'a'))
                reply = Series_Q_Reply(reply)
                delete_data(uid)
            elif search.getListByNos(msg) == [] :
                reply = FlexSendMessage(alt_text='查無結果',contents=noResult)
                line_bot_api.reply_message(event.reply_token,reply)
                delete_data(uid)
        elif datalist[0][2] == "nos_mode+P":
            if msg == "列出第"+get_var(uid, 'a')+"條的所有法條":
                reply = search.getFlexbyNos(get_var(uid, 'a'))
                reply = Series_Q_Reply(reply)
                delete_data(uid)
            elif "款" not in "".join(search.getListByNos(get_var(uid, 'a')+','+msg)):
                reply = search.getFlexbyNos(get_var(uid,'a')+','+msg)
                reply = Series_Q_Reply(reply)
                delete_data(uid)
            else:
                change_var(uid,'p',msg)
                change_state(uid, "nos_mode+P+S")
                reply = selects_nos_mode_P_S(event,uid,get_var(uid, 'a'),get_var(uid, 'p'))
        elif datalist[0][2] == "nos_mode+P+S": 
            if msg == "第"+get_var(uid, 'a')+"條第"+get_var(uid, 'p')+"項的所有法條" :
                reply = search.getFlexbyNos(get_var(uid, 'a')+','+get_var(uid,'p'))
                reply = Series_Q_Reply(reply)
                delete_data(uid)
            elif msg == "Previous-nos_mode_P":
                change_state(uid, "nos_mode+P")
                reply = selects_nos_mode_P(event,uid,get_var(uid, 'a'))
            else:
                change_var(uid,'s',msg)
                reply = search.getFlexbyNos(get_var(uid,'a')+','+get_var(uid,'p')+','+get_var(uid,'s'))
                reply = Series_Q_Reply(reply)
                delete_data(uid)
        elif datalist[0][2] == "nos_mode+S":
            change_var(uid,'s',msg)
            reply = search.getFlexbyNos(get_var(uid,'a')+',,'+get_var(uid,'s'))
            reply = Series_Q_Reply(reply)
            delete_data(uid)
        elif datalist[0][2] == "txt_mode":
            reply = search.newWordsSearch(msg)
            print("有在這裡喔")
            if len(reply.contents.body.contents) == 0:
                reply = FlexSendMessage(alt_text='查無結果',contents=noResult)
            else:
                reply = Series_Q_Reply(reply)
        elif datalist[0][2] == "dwiNdwdenterButtons":#酒毒駕進入面板
            if "DWI and DUD" in msg:
                reply = dwiNdwd(event)
                change_state(uid, "dwiNdwd")
            elif "The Newist Announcement" in msg:
                reply = ImageSendMessage(
                    original_content_url='https://raw.githubusercontent.com/laya1017/image/main/newisetAct.jpg',
                    preview_image_url='https://raw.githubusercontent.com/laya1017/image/main/newisetAct.jpg')
                delete_data(uid) #進入版面
            elif msg == "提審法":
                reply = HabeasCorpusAct(event)
                reply.quick_reply=dwiNdwdbuttonFilt(msg)
            elif msg == "三項權利(刑訴95條)":
                reply = CodeOfCriminalProcedure(event)
                reply.quick_reply=dwiNdwdbuttonFilt(msg)
            elif msg == "汽機車酒駕法條":
                reply = search.getFlexbyNos("35,1,1")
                reply.quick_reply = dwiNdwdbuttonFilt(msg)
            elif msg == "汽機車毒駕法條":
                reply = search.getFlexbyNos("35,1,2")
                reply.quick_reply = dwiNdwdbuttonFilt(msg)
            elif msg == "累犯法條":
                reply = search.getFlexbyNos("35,3")
                reply.quick_reply = dwiNdwdbuttonFilt(msg)
            elif msg == "汽機車酒駕拒測法條":
                reply = search.getFlexbyNos("35,4")
                reply.quick_reply = dwiNdwdbuttonFilt(msg)
            elif msg == "拒測累犯法條":
                reply = search.getFlexbyNos("35,5")
                reply.quick_reply = dwiNdwdbuttonFilt(msg)
            elif msg == "汽機車酒駕拒測告知":
                reply = YouShouldWarn(event)
                reply.quick_reply=dwiNdwdbuttonFilt(msg)
            elif msg == "慢車酒駕法條":
                reply = search.getFlexbyNos("73,2")
                reply.quick_reply = dwiNdwdbuttonFilt(msg)
            elif msg == "慢車酒駕拒測法條":
                reply = search.getFlexbyNos("73,3")
                reply.quick_reply = dwiNdwdbuttonFilt(msg)
            elif msg == "自動點火裝置(酒精鎖)":
                reply = search.getFlexbyNos("35-1")
                reply.quick_reply = dwiNdwdbuttonFilt(msg)
            elif msg == "回到酒(毒)駕區":
                reply = dwiNdwdenterButtons(event, msg)
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
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
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
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
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
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
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
        elif datalist[0][2] == "dwimode_CNS_Ex": #酒駕超標舉發
            if msg == "First Violation":
                reply = search.getFlexbyNos('35,1,1')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與慢車酒駕比較",text="SMV Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Recidivism":
                reply = search.getFlexbyNos('35,3')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Dos and Don\'ts":
                reply = TextSendMessage(
                    text = "1.檢測流程：\n(1)原則於現場攔檢測試。如現場無法或不宜實施檢測時，得向受測者說明，請其至勤務處所或適當場所檢測。\n(2)詢問飲用酒類結束時間，如已達15分鐘以上者，即予檢測。\n(3)受測者不告知時間或距結束時間未達15分鐘者，告知其可於漱口或距該結束時間達15分鐘後進行檢測。\n(4)有請求漱口者，提供漱口。\n(5)告知受測者儀器檢測之流程，請其口含吹嘴連續吐氣至儀器顯示取樣完成。\n(6)受測者吐氣不足致儀器無法完成取樣時，應重新檢測。\n(7)因儀器問題或受測者未符合檢測流程，致儀器檢測失敗，應向受測者說明檢測失敗原因，請其重新接受檢測。\n(8)檢測成功後，不論有無超過規定標準，不得實施第二次檢測。\n(9)遇檢測結果出現明顯異常情形時，應停止使用該儀器並改用其他儀器檢測，並應留存原異常之紀錄。\n(10)檢測後，應告知受測者檢測結果，並請其於檢測結果紙上簽名確認。\n(11)拒絕簽名時，應記明事由。\n(12)有客觀事實足認受測者無法實施吐氣酒精濃度檢測時，得經其同意後送由受委託醫療或檢驗機構對其實施血液之採樣及測試檢定。\n2、標準值：\n(1)道安規則114條：飲用酒類或其他類似物後其吐氣所含酒精濃度達0.15mgl或血液中酒精濃度達0.03%以上。\n(2)刑法185-3條：吐氣所含酒精濃度達0.25mg/l或血液中酒精濃度達0.05%以上\n3.勸導要件：\n(1)駕駛汽車或慢車經測試檢定，其吐氣所含酒精濃度超過規定之標準值(0.15mgl或血液中酒精濃度達0.03%)未逾0.02mg/l。\n(2)行為人發生交通事故時，仍得舉發。\n4.租賃車部分：\n租賃車業者已盡告知本條處罰規定之義務，汽機車駕駛人仍駕駛汽機車違反第1項、第2項至第5項規定之一者，依其各行為所處之罰鍰加罰1/2。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Owner":
                reply = search.getFlexbyNos('35,7')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Passenger":
                reply = search.getFlexbyNos('35,8')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
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
                reply = search.getFlexbyNos("73,2"),
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
        elif datalist[0][2] == "dwimode_CNS_Re":#汽機車拒測舉發
            if msg == "First Violation":
                reply = search.getFlexbyNos('35,4')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與慢車拒測比較",text="SMV Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "SMV Violation":
                reply = search.getFlexbyNos("73,3")
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Recidivism":
                reply = search.getFlexbyNos('35,5')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwimode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Notification":
                reply = TextSendMessage(
                    text = "⊙拒絕接受酒精濃度檢定告知事項：\n一、初次違反：\n1.罰鍰：新台幣18萬元\n2.吊銷駕駛執照\n3.應受道路交通安全講習\n4.當場移置保管車輛\n5.吊扣所駕車輛牌照2年\n6.「如」租賃車業者已告知本條處罰規定，依所處罰鍰加重1/2。\n二、「如」再次違反：\n1.罰鍰：10年內第2次違反處新台幣36萬元，第3次以上按前次處罰加罰18萬元。\n2.吊銷駕駛執照\n3.應受道路交通安全講習\n4.當場移置保管車輛\n5.吊扣所駕車輛牌照2年\n6.公布姓名、照片及違法事情★\n7.「如」租賃車業者已告知本條處罰規定，依所處罰鍰加重1/2。",
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
                    text = "I  .對汽車駕駛人實施本條例第35條第1項第1款測試之檢定時，應以酒精測試儀器檢測且實施檢測過程應全程連續錄影，並依下列程序處理：\n1.實施檢測，應於攔檢現場為之。但於現場無法或不宜實施檢測時，得向受測者說明，請其至勤務處所或適當場所檢測。\n2.詢問受測者飲用酒類或其他類似物結束時間，其距檢測時已達15分鐘以上者，即予檢測。但遇有受測者不告知該結束時間或距該結束時間未達15分鐘者，告知其可於漱口或距該結束時間達15分鐘後進行檢測；有請求漱口者，提供漱口。\n3.告知受測者儀器檢測之流程，請其口含吹嘴連續吐氣至儀器顯示取樣完成。受測者吐氣不足致儀器無法完成取樣時，應重新檢測。\n4.因儀器問題或受測者未符合檢測流程，致儀器檢測失敗，應向受測者說明I２.檢測失敗原因，請其重新接受檢測。\nII .實施前項檢測後，應告知受測者檢測結果，並請其在儀器列印之檢測結果紙上簽名確認。拒絕簽名時，應記明事由。\nIII.實施第一項檢測成功後，不論有無超過規定標準，不得實施第二次檢測。但遇檢測結果出現明顯異常情形時，應停止使用該儀器，改用其他儀器進行檢測，並應留存原異常之紀錄。\nIV .有客觀事實足認受測者無法實施吐氣酒精濃度檢測時，得於經其同意後，送由受委託醫療或檢驗機構對其實施血液之採樣及測試檢定。\nV  .汽車駕駛人拒絕配合實施本條例第35條第1項第1款檢測者，應依下列規定處理：\n1.告知拒絕檢測之法律效果：\n(1)拒絕接受酒精濃度測試檢定者，處新臺幣18萬元罰鍰，吊銷駕駛執照及吊扣該車輛牌照2年；肇事致人重傷或死亡者，並得沒入車輛。\n(2)於10年內第2次違反本條例第35條第4項規定者，處新臺幣36萬元罰鍰，第3次以上者按前次違反本項所處罰鍰金額加罰新臺幣18萬元，吊銷駕駛執照，公路主管機關得公布姓名、照片及違法事實，並吊扣該車輛牌照2年；肇事致人重傷或死亡者，並得沒入車輛。\n(3)租賃車業者已盡告知本條例第35條處罰規定之義務，汽車駕駛人仍有前二目情形者，依所處罰鍰加罰1/2。\n二、依本條例第35條第4項或第5項製單舉發。",
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
                reply = search.getFlexbyNos("73,2")
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與汽機車酒駕規定比較", text="CNS Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "CNS Violation":
                reply = search.getFlexbyNos('35,1,1')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "SMV Definition":
                reply = TextSendMessage(
                    text="道交條例69條1項：\n慢車種類及名稱如下：\n1.自行車：\n(1)腳踏自行車。\n(2)電動輔助自行車：指經型式審驗合格，以人力為主、電力為輔，最大行駛速率在每小時25公里以下，且車重在40公斤以下之二輪車輛。\n(3)電動自行車：指經型式審驗合格，以電力為主，最大行駛速率在每小時25公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n2.其他慢車：\n(1)人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛速率在每小時25公里以下，且行駛於指定路段之慢車。\n(2)獸力行駛車輛：指牛車、馬車等。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Criminal Code Question":
                reply = TextSendMessage(
                    text="依據法務部法檢字第1000014063號函：\n要旨：\n參照刑法第 185條之 3規定，「腳踏自行車」「電動輔助自行車」「電動自行車」是否符合該條之「動力交通工具」，端視其推動是否以電力或引擎動力等作用而斷\n主旨：就所詢刑法第 185條之 3「動力交通工具」之適用範圍乙案，復如說明，請查照。\n說明：\n一、復貴署100年5月23日警署交字第1000117598號函。\n二、刑法第185條之3之「動力交通工具」，係指交通工具之推動是以電力或引擎動力等作用者，至其為蒸汽機、內燃機，抑或係柴油、汽油、天然氣、核子、電動，均非所問。又所謂交通工具不限於陸路交通工具，尚包含水上、海上、空中或鐵道上之交通工具。所詢之「腳踏自行車」「電動輔助自行車」「電動自行車」是否符合刑法第185條之3之「動力交通工具」，端視其推動是否以電力或引擎動力等作用而斷。惟如涉及具體個案，應由承辦之檢察官或法官依職權判斷。\n正本：內政部警政署\n副本：本部檢察司、本部檢察司一股",
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
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
        elif datalist[0][2] == "dwimode_SMV_Re":
            if msg == "Violation":
                reply = search.getFlexbyNos('73,3')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與汽機車拒測規定比較", text="CNS Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "CNS Violation":
                reply = search.getFlexbyNos('35,4')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="dwimode_SMV_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "SMV Definition":
                reply = TextSendMessage(
                    text="道交條例69條1項：\n慢車種類及名稱如下：\n1.自行車：\n(1)腳踏自行車。\n(2)電動輔助自行車：指經型式審驗合格，以人力為主、電力為輔，最大行駛速率在每小時25公里以下，且車重在40公斤以下之二輪車輛。\n(3)電動自行車：指經型式審驗合格，以電力為主，最大行駛速率在每小時25公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n2.其他慢車：\n(1)人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛速率在每小時25公里以下，且行駛於指定路段之慢車。\n(2)獸力行駛車輛：指牛車、馬車等。",
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
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
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
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
        elif datalist[0][2] == "dwdmode_CNS_Ex": #毒駕超標舉發
            if msg == "First Violation":
                reply = search.getFlexbyNos('35,1,2')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="慢車沒有毒駕處罰？",text="SMV Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "SMV Violation":
                reply = TextSendMessage(
                    text="一、慢車於道路交通管理處罰條例第73條2項及3項皆處罰為「\"酒精\"濃度超標」及「拒絕\"酒精\"濃度測試」，且於同法中並\"無\"規定服用藥物駕駛之處罰。\n二、但經尿液或血液中檢測有\"毒品、迷幻藥、麻醉藥品及其相類似之管制藥品\"成分時，則屬於刑法185-3條第1項「服用毒品、麻醉藥品或其他相類之物，致不能安全駕駛」，此情況建議將行為人(駕駛人)精神狀況以攝影器材紀錄，如可製作觀測表之情況則更好。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="道交條例73條2項及3項", text="Check 73-2 and 73-3")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Check 73-2 and 73-3":
                reply = search.getByNos("73,2")+"\n"+search.getByNos("73,3").strip(),
                reply.quick_reply = QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="回上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Recidivism":
                reply = search.getFlexbyNos('35,3')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Dos and Don\'ts":
                reply = TextSendMessage(
                    text = "一、標準值(供參考用)：\n濫用藥物尿液檢驗作業準則18條：\nI 初步檢驗結果在閾值以上或有疑義之尿液檢體，應再進行確認檢驗。確認檢驗結果在下列閾值以上者，應判定為陽性：\n1、安非他命類藥物：\n（1）安非他命：500ng/mL。\n（2）甲基安非他命：甲基安非他命500ng/mL，且其代謝物安非他命之濃度在100ng/mL以上。\n（3）3,4-亞甲基雙氧甲基安非他命（MDMA）：500ng/mL。同時檢出MDMA及MDA時，兩種藥物之個別濃度均低於500ng/mL，但總濃度在500ng/mL以上者，亦判定為MDMA陽性。\n（4）3,4-亞甲基雙氧安非他命（MDA）：500ng/mL。\n（5）3,4-亞甲基雙氧-N-乙基安非他命（MDEA）：500ng/mL。\n2、海洛因、鴉片代謝物：\n（1）嗎啡：300ng/mL。\n（2）可待因：300ng/mL。\n3、大麻代謝物（四氫大麻酚-9-甲酸，Delta-9-tetrahydrocannabinol-9-carboxylicacid）：15ng/mL。\n4、古柯鹼代謝物（苯甲醯基愛哥寧，Benzoylecgonine）：150ng/mL。\n5、愷他命代謝物：\n（一）愷他命（Ketamine）：100ng/mL。同時檢出愷他命及去甲基愷他命（Norketamine）時，兩種藥物之個別濃度均低於100ng/mL，但總濃度在100ng/mL以上者，亦判定為愷他命陽性。\n（二）去甲基愷他命：100ng/mL。\nII、前項以外之濫用藥物或其代謝物，依衛生福利部食品藥物管理署公告之濃度作為判定檢出之閾值。未有公告者，檢驗機構得依其分析方法最低可定量濃度訂定適當閾值。\n二、建議：\n此情況建議施測前將行為人(駕駛人)精神狀況以攝影器材紀錄、製作觀測表，如涉嫌隨案移請地方檢察署檢察官認定。\n三、租賃車部分：\n1.租賃車業者已盡告知本條處罰規定之義務，汽機車駕駛人仍駕駛汽機車違反第一項、第三項至第五項規定之一者，依其各行為所處之罰鍰加罰1/2。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Owner":
                reply = search.getFlexbyNos('35,7')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
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
                reply = search.getFlexbyNos("35,8")
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
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
                reply = search.getFlexbyNos("73,2")
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Ex")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
        elif datalist[0][2] == "dwdmode_CNS_Re":
            if msg == "First Violation":
                reply = search.getFlexbyNos('35,4')
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="與慢車拒測比較",text="SMV Violation")),
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "SMV Violation":
                reply = search.getFlexbyNos("73,3"),
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Recidivism":
                reply = search.getFlexbyNos('35,5'),
                reply.quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_CNS_Re")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
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
                    text = "I  .對汽車駕駛人實施本條例第35條第1項第1款測試之檢定時，應以酒精測試儀器檢測且實施檢測過程應全程連續錄影，並依下列程序處理：\n1.實施檢測，應於攔檢現場為之。但於現場無法或不宜實施檢測時，得向受測者說明，請其至勤務處所或適當場所檢測。\n2.詢問受測者飲用酒類或其他類似物結束時間，其距檢測時已達15分鐘以上者，即予檢測。但遇有受測者不告知該結束時間或距該結束時間未達15分鐘者，告知其可於漱口或距該結束時間達15分鐘後進行檢測；有請求漱口者，提供漱口。\n3.告知受測者儀器檢測之流程，請其口含吹嘴連續吐氣至儀器顯示取樣完成。受測者吐氣不足致儀器無法完成取樣時，應重新檢測。\n4.因儀器問題或受測者未符合檢測流程，致儀器檢測失敗，應向受測者說明I２.檢測失敗原因，請其重新接受檢測。\nII .實施前項檢測後，應告知受測者檢測結果，並請其在儀器列印之檢測結果紙上簽名確認。拒絕簽名時，應記明事由。\nIII.實施第一項檢測成功後，不論有無超過規定標準，不得實施第二次檢測。但遇檢測結果出現明顯異常情形時，應停止使用該儀器，改用其他儀器進行檢測，並應留存原異常之紀錄。\nIV .有客觀事實足認受測者無法實施吐氣酒精濃度檢測時，得於經其同意後，送由受委託醫療或檢驗機構對其實施血液之採樣及測試檢定。\nV  .汽車駕駛人拒絕配合實施本條例第35條第1項第1款檢測者，應依下列規定處理：\n1.告知拒絕檢測之法律效果：\n(1)拒絕接受酒精濃度測試檢定者，處新臺幣18萬元罰鍰，吊銷駕駛執照及吊扣該車輛牌照2年；肇事致人重傷或死亡者，並得沒入車輛。\n(2)於10年內第2次違反本條例第35條第4項規定者，處新臺幣36萬元罰鍰，第3次以上者按前次違反本項所處罰鍰金額加罰新臺幣18萬元，吊銷駕駛執照，公路主管機關得公布姓名、照片及違法事實，並吊扣該車輛牌照2年；肇事致人重傷或死亡者，並得沒入車輛。\n(3)租賃車業者已盡告知本條例第35條處罰規定之義務，汽車駕駛人仍有前二目情形者，依所處罰鍰加罰1/2。\n二、依本條例第35條第4項或第5項製單舉發。",
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
                reply = dwdmode_CNS_Ex(event)
                change_state(uid, "dwdmode_CNS_Ex")
            elif msg == "Back to dwdmode_CNS_Re":
                reply = dwdmode_CNS_Re(event)
            elif msg == "Back to dwdmode":
                reply = dwdmode(event) 
                change_state(uid, "dwdmode")
            else :
                reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
        elif datalist[0][2] == "dwdmode_SMV":
            if msg == "SMV Definition":
                reply = TextSendMessage(
                    text="道交條例69條1項：\n慢車種類及名稱如下：\n1.自行車：\n(1)腳踏自行車。\n(2)電動輔助自行車：指經型式審驗合格，以人力為主、電力為輔，最大行駛速率在每小時25公里以下，且車重在40公斤以下之二輪車輛。\n(3)電動自行車：指經型式審驗合格，以電力為主，最大行駛速率在每小時25公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n2.其他慢車：\n(1)人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛速率在每小時25公里以下，且行駛於指定路段之慢車。\n(2)獸力行駛車輛：指牛車、馬車等。",
                    quick_reply=QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="上一步", text="Back to dwdmode_SMV")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
                    )
            elif msg == "Check 73-2 and 73-3":
                reply = search.getFlexbyNos("73,2")
                reply.contents.body.contents += search.getFlexbyNos("73,3").contents.body.contents
                reply.quick_reply = QuickReply(
                        items=[
                        QuickReplyButton(action=MessageAction(label="回上一步", text="Back to dwdmode_SMV")),
                        QuickReplyButton(action=MessageAction(label="離開", text="Exit"))
                        ]
                        )
            elif msg == "Back to dwdmode":
                reply = dwdmode(event) #回到汽機車毒駕面板
                change_state(uid, "dwdmode")
            elif msg == "Back to dwdmode_SMV":
                reply = dwdmode_SMV(event)
            else:
                reply = TextSendMessage(text="已離開~")
                delete_data(uid)
        else:
            reply = TextSendMessage(text="不會使用嗎？點選下面選單就知道囉！")
    line_bot_api.reply_message(event.reply_token,reply)
if __name__ == "__main__":
    app.run()
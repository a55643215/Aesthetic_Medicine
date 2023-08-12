from line_bot_api import *
from urllib.parse import parse_qsl


#預約相關功能都會寫在這邊
services = {
    1:{
        'category':'醫美',
        'img_url':'https://i.imgur.com/iYK9HG8.jpg',
        'title':'減肥/瘦身',
        'duration':'30min',
        'description' : '提供減肥瘦身相關詢問',
        'price':100,
        'post_url':'https://google.com'
    },
    2: {
        'category':'醫美',
        'img_url':'https://i.imgur.com/iYK9HG8.jpg',
        'title':'美白',
        'duration':'60min',
        'description' : '使肌膚退去黑色素沈澱，達到身體美白效果',
        'price':2000,
        'post_url':'https://google.com'
    },
    3: {
        'category':'醫美',
        'img_url':'https://i.imgur.com/iYK9HG8.jpg',
        'title':'除疤',
        'duration':'30min',
        'description' : '將擦傷/切割傷/外科傷口疤痕去除',
        'price':6000,
        'post_url':'https://google.com'
    },
    4: {
        'category':'醫美',
        'img_url':'https://i.imgur.com/iYK9HG8.jpg',
        'title':'豐胸',
        'duration':'30min',
        'description' : '提供自體隆乳/魔滴乳膠隆乳諮詢',
        'price':200,
        'post_url':'https://google.com'
    }
    }

def service_catgory_event(event):
     image_carousel_template_message = TemplateSendMessage(
          alt_text = '請選擇想服務類別',
          template = ImageCarouselTemplate(
            columns = [
                 ImageCarouselColumn(
                    image_url = 'https://i.imgur.com/iYK9HG8.jpg',
                    action = PostbackAction(
                        label = '醫美',
                        display_text = '醫美',
                        data = 'action=service&category=醫美'
                    )
                 )
            ]
          )
     )
     line_bot_api.reply_message(
          event.reply_token,
          [image_carousel_template_message]
     )



def service_event(event):
    #底下三個要等上面的service建立後才寫，主要是要跑service的服務
    #data = dict(parse_qsl(event.postback.data))
    #bubbles=[]
    #for service_id in services:

    data = dict(parse_qsl(event.postback.data))
    bubbles = []

    for service_id in services:
            if services[service_id]['category'] == data['category']:
                service = services[service_id]
                bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": service['img_url']
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": service['title'],
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": service['duration'],
                        "size": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": service['description'],
                        "margin": "lg",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"NT$ {service['price']}",
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl",
                            "flex": 0
                        }
                        ],
                        "margin": "xl"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                        "type": "postback",
                        "label": "預約",
                        "data": f"action=select_date&service_id={service_id}",
                        "displayText": f"我想預約【{service['title']} {service['duration']}】"
                        },
                        "color": "#b28530"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "了解詳情",
                        "uri": service['post_url']
                        }
                    }
                    ]
                }
                }

                bubbles.append(bubble)

    flex_message = FlexSendMessage(
         alt_text = '請選擇預約項目',
         contents={
              "type":"carousel",
              "contents":bubbles
         }
    )

    line_bot_api.reply_message(
         event.reply_token,
         [flex_message]
    )


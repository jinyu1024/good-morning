from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()

city = os.environ['CITY']
birthday = os.environ['KAOYAN']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], weather['temp'], weather['low'], weather['high'], weather['date']



def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("http://api.tianapi.com/zaoan/index?key=611d2adcfc2316f0ded280cd74407d8a")

  return words

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, low_temp, high_temp, day = get_weather()
data = {"today":{"value":day, "color":get_random_color()},"weather":{"value":wea, "color":get_random_color()},"low_temp":{"value":low_temp, "color":get_random_color()},"high_temp":{"value":high_temp, "color":get_random_color()},
        "kaoyan":{"value":get_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)

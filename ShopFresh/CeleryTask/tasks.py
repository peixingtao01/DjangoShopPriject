# 这个文件是返回到运行之后的那个所谓的异步
from __future__ import absolute_import
from ShopFresh.celery import app
import json,requests
@app.task
def taskExample():
    print('send email ok!')
    return 'send email ok!'
@app.task
def add(x=1,y=2):
    return x+y
@app.task
def DingTalk():
    url = 'https://oapi.dingtalk.com/robot/send?access_token=105ae687b7693acc3ae752652b41ad542561f51d79d07421e3cf7167571e5f04'
    headers = {
        'Content-Type':'application/json',
        'Chartset':'utf-8'
    }
    requests_data = {
        'msgtype':'text',
        'text':{
            'content':'今天又是充满希望的一天'
        },
        'at':{
            'atMobiles':[

            ],
        },
        'isAtAll':True
    }
    sendData = json.dumps(requests_data)
    response = requests.post(url,headers=headers,data=sendData)
    content = response.json()
    print(content)
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#people's data

numstr_list = ['031', '032', '033', '034', '035', '036', '037', '038', '039']
people_disc = {'031': '031-未回報',
               '032': '032-未回報',
               '033': '033-未回報',
               '034': '1.學號：034\n2.姓名：洪振惟\n3.電話：0929719266\n4.所在地：壽司郎\n5.做什麼：吃壽司\n6.陪同人：朋友\n7.驗證人：朋友\n',
               '035': '035-未回報',
               '036': '036-未回報',
               '037': '037-未回報',
               '038': '038-未回報',
               '039': '039-未回報',
               }
# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    receive_message = event.message.text
    if len(receive_message) < 3:
        receive_message = receive_message + '!!!'
    tmp = receive_message.split('\n')
    key = tmp[0][-3] + tmp[0][-2] + tmp[0][-1]
    #print('key = {}'.format(key))

    if key in numstr_list:
        replying_message = ''
        people_disc[key] = receive_message
        tmp = list(people_disc.values())
        for keys in people_disc.keys():
            replying_message = replying_message + str(people_disc[keys]) + '\n------------------------\n'

        print(replying_message)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=replying_message)
        )
    elif receive_message == '回報重置':
        replying_message = ''

        for keys in people_disc.keys():
            people_disc[keys] = str(keys) +'-未回報'
            replying_message = replying_message + str(people_disc[keys]) + '\n------------------------\n'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=replying_message)
        )
    elif receive_message.find('跑跑') != -1:
         reply_candidates = ['你很勇嘛','給我站起來','輕話重聽', '你很勇嘛!']
         random_index = random.randrange(len(reply_candidates))
         line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_candidates[random_index])
        )

if __name__ == "__main__":
    app.run()
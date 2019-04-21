# -*- coding: utf-8 -*-
'''
@author: DipperStar
@mail: ssr@yinheng.xyz
'''
from pocketapi import API
from mongo import MongoDB
from cqapi import CQclient
from Scheduler import SCHEDULE
import time
import json

false = 'flase'
true = 'true'
null = 'null'

class POCKET48(API, CQclient, SCHEDULE):
    '''
    口袋48模块
    : func _todo: 查询房间消息
    '''
    def __init__(self, mobile, password, membername):
        super().__init__(mobile, password, membername)
        CQclient.__init__(self)
        SCHEDULE.__init__(self)
        self.dbchat = MongoDB('Poket48', str(self.roomId))
        self.msgType = dict(TEXT=self.text,VIDEO=self.video,\
                            IMAGE=self.image,AUDIO=self.audio)

    def update_chat(self):
        list_msg = []
        for chat in self.chatroom():
            if self.dbchat.update(chat, upsert=True) == 'success':
                list_msg.append(chat)
        list_msg.reverse()
        return list_msg

    def format_chat(self, msg):
        if msg['msgType'] in self.msgType:
            return self.msgType[msg['msgType']](msg)
        else:
            return '未定义类型消息...'

    def stamp2str(self, stamp):
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(stamp/1000))
        return time_str

    def text(self, msg):
        extInfo = json.loads(msg['extInfo'])
        nickName = extInfo['user']['nickName']
        if extInfo['messageType'] == 'TEXT':
            msg = ('%s：%s\n%s' % (
                nickName,
                extInfo['text'],
                self.stamp2str(msg['msgTime'])))
        elif extInfo['messageType'] == 'REPLY':
            msg = ('%s：%s\n%s：%s\n%s' % (
                extInfo['replyName'], extInfo['replyText'],
                nickName, extInfo['text'],
                self.stamp2str(msg['msgTime'])))
        elif extInfo['messageType'] == 'LIVEPUSH':
            playStreamPath, playDetail = self.livedetail(extInfo['liveId'])
            if not playStreamPath:
                playStreamPath = "暂无"
            msg = [{'type': 'text', 'data': {
                'text': '小偶像开直播啦 \n直播标题：%s \n' % extInfo['liveTitle']}},
                   {'type': 'image', 'data': {
                       'file': 'https://source.48.cn%s' % extInfo['liveCover']}},
                   {'type': 'text', 'data': {
                     'text': '直播地址：https://h5.48.cn/2019appshare/memberLiveShare/index.html?id=%s\n推流地址：%s\n开始时间：%s' % (
                           extInfo['liveId'],
                           playStreamPath,
                           self.stamp2str(msg['msgTime']))}}
                   ]
        elif extInfo['messageType'] == 'FLIPCARD':
            msg = ('%s：%s\n问题内容：%s\n%s' % (
                nickName, extInfo['answer'],
                extInfo['question'], self.stamp2str(msg['msgTime'])))
        else:
            msg = '有未知格式的文字消息'
        return msg

    def video(self, msg):
        bodys = json.loads(msg['bodys'])
        extInfo = eval(msg['extInfo'])
        msg = [{'type': 'text', 'data': {
            'text': '%s：视频消息' % extInfo['user']['nickName']}},
               {'type': 'record', 'data': {
                   'file': '%s' % bodys['url']}},
               {'type': 'text', 'data': {
                   'text': '\n%s' % self.stamp2str(msg['msgTime'])}}
               ]
        return msg

    def audio(self, msg):
        bodys = json.loads(msg['bodys'])
        extInfo = eval(msg['extInfo'])
        msg = [{'type': 'text', 'data': {
            'text': '%s：语音消息' % extInfo['user']['nickName']}},
               {'type': 'record', 'data': {
                   'file': '%s' % bodys['url']}},
               {'type': 'text', 'data': {
                   'text': '\n%s' % self.stamp2str(msg['msgTime'])}}
               ]
        return msg

    def image(self, msg):
        bodys = json.loads(msg['bodys'])
        extInfo = eval(msg['extInfo'])
        msg = [{'type': 'text', 'data': {
            'text': '%s：图片消息' % extInfo['user']['nickName']}},
               {'type': 'image', 'data': {
                   'file': '%s' % bodys['url']}},
               {'type': 'text', 'data': {
                   'text': '%s' % self.stamp2str(msg['msgTime'])}}
               ]
        return msg

    def _todo(self):
        for chat in self.update_chat():
            msg = self.format_chat(chat)
            self.single_msg(msg)
            time.sleep(1)

if __name__ == '__main__':
    lishanshan = POCKET48(urs1, psw1, '李姗姗')
    lishanshan.interval_time = 120
    xiongxinyao = POCKET48(urs1, psw1, '熊心瑶')
    xiongxinyao.interval_time = 240
    fangqi = POCKET48(urs1, psw1, '方琪')
    fangqi.interval_time = 240
    lishanshan.run()
    xiongxinyao.run()
    fangqi.run()
    schedul = SCHEDULE()
    schedul.block()  # 阻塞
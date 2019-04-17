# -*- coding: utf-8 -*-
'''
@author: DipperStar
@mail: ssr@yinheng.xyz
'''
import requests
import json
import getopt
import sys
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class API(object):
    '''
    口袋48 api
    : func searchroom: 查找指定成员房间信息
    : func login: 登录
    : func chatroom: 查询房间消息
    '''
    def __init__(self, mobile, password, membername):
        '''
        :param mobile: 电话 int or string
        :param password: 密码 string
        :param membername: 成员全名 string
        '''
        self.mobile = mobile
        self.password = password
        self.membername = membername
        self.hastoken = dict(timestamp=0)
        self.headers = {'Host': 'pocketapi.48.cn',
                                'accept': '*/*',
                                'Accept-Language': 'zh-Hans-CN;q=1',
                                'User-Agent': 'PocketFans201807/6.0.0 (iPhone; iOS 12.2; Scale/2.00)',
                                'Accept-Encoding': 'gzip, deflate',
                                'appInfo': '{"vendor":"apple","deviceId":"0","appVersion":"6.0.0","appBuild":"190409","osVersion":"12.2.0","osType":"ios","deviceName":"iphone","os":"ios"}',
                                'Content-Type': 'application/json;charset=utf-8',
                                'Connection': 'keep-alive',
                                }
        dic_data = self.searchroom()
        self.ownerId, self.roomId = dic_data['ownerId'], dic_data['roomId']

    @property
    def _token(self):
        '''
        获取token,超过1天则重新登录
        : return: token string
        '''
        if self._nowtime - self.hastoken['timestamp'] > 3600*24:
            token = self.login()
            self.hastoken = dict(timestamp=self._nowtime, token=token)
        return self.hastoken['token']

    @property
    def _nowtime(self):
        '''
        当前时间戳
        : return: 当前时间戳 float
        '''
        return time.time()

    def searchroom(self):
        '''
        获取成员房间信息
        : param membername: 成员全名
        : return: 成员房间信息 json roomName 房间名, ownerName 成员名, roomId 房间名, ownerId 成员编号
        '''
        url = 'https://pocketapi.48.cn/im/api/v1/im/search'
        data = {
                    'name': self.membername
                    }
        try:
            response = requests.post(url, json=data, headers=self.headers, verify=False).json()['content']['data'][0]
            return dict(roomName=response['targetName'], ownerName=response['ownerName'], roomId=response['targetId'],
                        ownerId=response['ownerId'])
        except Exception as e:
            raise e

    def login(self):
        '''
        登录
        : param mobile: 手机号
        : param password: 密码
        : return token: 登录token string
        '''
        try:
            url = 'https://pocketapi.48.cn/user/api/v1/login/app/mobile'
            data = {
                        "pwd": str(self.password),
                        "mobile": str(self.mobile),
                        }
            res = requests.post(url, headers=self.headers, json=data, verify=False).json()
            return res['content']['token']
        except Exception as e:
            raise e

    def chatroom(self):
        '''
        获取成员房间消息
        : param roomId: 房间编号
        : param ownerId: 成员编号
        : return: 发言信息 json
        '''
        url = 'https://pocketapi.48.cn/im/api/v1/chatroom/msg/list/homeowner'
        false = 'false'
        headers = self.headers
        headers.update({'token': self._token})
        data = dict(needTop1Msg=False, roomId=str(self.roomId), ownerId=str(self.ownerId))
        try:
            res = requests.post(url, headers=headers, json=data).json()['content']['message']
            return res
        except Exception as e:
            raise e

if  __name__ == '__main__':
    myapi = API()
    for x in myapi.chatroom():
        print(x)
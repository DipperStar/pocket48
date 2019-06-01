# -*- coding: utf-8 -*-
'''
@author: DipperStar
@mail: ssr@yinheng.xyz
'''
import requests
import urllib3
import time
import random
from cryptography.fernet import Fernet
from mongo import MongoDB
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class API(object):
    '''
    口袋48 api
    : func searchroom: 查找指定成员房间信息
    : func login: 登录
    : func chatroom: 查询房间消息
    : func livedetail: 获取直播详情
    '''

    def __init__(self):
        '''
        :param mobile: 电话 int or string
        :param password: 密码 string
        :param membername: 成员列表 string
        '''
        self.color = ['#FEEEED', '##CCFFFF', '#CCFFCC', '#E0FFFF', '#F0FFF0', '#F0F8FF', '#FFF0F5', '#FFFAFA',
                      '#F0FFFF', '#FFF5EE', '#E6E6FA', '#FFC0CB']
        self.dbtoken = MongoDB('Pocket48', 'dbtoken')
        self.key = b'1O8zgva3PlT_Evikm61A97wsWZ0JlTGSNEiRc0S7rCY='
        self.Fernet = Fernet(self.key)
        self.source_url = 'https://source.48.cn'
        self.headers = {
            'Host': 'pocketapi.48.cn',
            'accept': '*/*',
            'Accept-Language': 'zh-Hans-CN;q=1',
            'User-Agent': 'PocketFans201807/6.0.0 (iPhone; iOS 12.2; Scale/2.00)',
            'Accept-Encoding': 'gzip, deflate',
            'appInfo': '{"vendor":"apple","deviceId":"0", \
                                "appVersion":"6.0.0","appBuild":"190409", \
                                "osVersion":"12.2.0","osType":"ios", \
                                "deviceName":"iphone","os":"ios"}',
            'Content-Type': 'application/json;charset=utf-8',
            'Connection': 'keep-alive',
        }

    def token(self, token):
        '''
        验证token
        : return: token string
        '''
        hastoken = list(self.dbtoken.find({'token': token}, projection={'_id': 0}))
        if not hastoken:
            return False
        elif self._nowtime - hastoken[0]['timestamp'] > 3600 * 24 * 7:
            self.dbtoken.remove({'token': token})
            return False
        else:
            return hastoken[0]

    @property
    def _nowtime(self):
        '''
        当前时间戳
        : return: 当前时间戳 float
        '''
        return time.time()

    def addmember(self, name, token):
        '''
        添加成员
        : param name: 成员全名
        : param token: token
        : return: token及附带的信息 response_object json
        '''
        url = 'https://pocketapi.48.cn/im/api/v1/im/search'
        data = {
            'name': name
        }
        try:
            response = requests.post(url, json=data, headers=self.headers,
                                     verify=False).json()['content']['data'][0]
            temp = dict(roomName=response['targetName'], ownerName=response['ownerName'], ownerId=response['ownerId'],
                        roomId=response['targetId'], color=random.choice(self.color), icon=self.source_url+response['icon'][0])
            self.dbtoken.update({'token': token}, {'$addToSet': {'member': temp}}, upsert=True)
            return list(self.dbtoken.find({'token': token}, projection={'_id': 0}))[0]
        except Exception as e:
            raise e

    def removemember(self, roomId, token):
        '''
        删除成员
        : param roomId:
        : param token:
        : return:
        '''
        try:
            self.dbtoken.update({'token': token}, {'$pull': {'member':{'roomId':roomId}}})
            return list(self.dbtoken.find({'token': token}, projection={'_id': 0}))[0]
        except Exception as e:
            raise e

    def removetoken(self, token):
        '''
        删除token
        : param roomId:
        : param token:
        : return:
        '''
        try:
            self.dbtoken.remove({'token': token})
            return True
        except Exception as e:
            raise e

    def login(self, mobile, password):
        '''
        登录
        : param mobile: 手机号
        : param password: 密码
        : return token: 登录token string
        '''
        try:
            token = str(mobile)
            hastoken = list(self.dbtoken.find({'token': token}, projection={'_id': 0}))
            if not hastoken:
                url = 'https://pocketapi.48.cn/user/api/v1/login/app/mobile'
                data = {
                    "pwd": str(password),
                    "mobile": str(mobile),
                }
                res = requests.post(
                    url,
                    headers=self.headers,
                    json=data,
                    verify=False).json()['content']
                token48 = res['token']
                nickname = res['userInfo']['nickname']
                avatar = self.source_url + res['userInfo']['avatar']
                temp = dict(token48=token48, token=str(mobile), member=[], timestamp=self._nowtime, avatar=avatar, nickname=nickname)
                self.dbtoken.update(temp, {'$set': temp}, upsert=True)
                return temp
            else:
                return hastoken[0]
        except Exception as e:
            raise e

    def chatroom(self, token):
        '''
        获取成员房间消息
        : param roomId: 房间编号
        : param ownerId: 成员编号
        : return: 发言信息 json
        '''
        url = 'https://pocketapi.48.cn/im/api/v1/chatroom/msg/list/homeowner'
        headers = self.headers
        res = list(self.dbtoken.find({'token': token}))[0]
        token48 = res['token48']
        list_member = res['member']
        if not list_member:
            return list_member
        headers.update({'token': token48})
        return_data = []
        for member in list_member:
            data = dict(
                needTop1Msg=False, roomId=str(
                    member['roomId']), ownerId=str(
                    member['ownerId']))
            try:
                res = requests.post(url, headers=headers, json=data).json()[
                    'content']['message']
                color = member['color']
                return_data.append({'color': color, 'res': res})
            except Exception as e:
                raise e
        return return_data

    def livedetail(self, liveId):
        '''
        获取直播详情
        :param liveId: 直播编号 int
        :return: playStreamPath string, response
        '''
        url = "https://pocketapi.48.cn/live/api/v1/live/getLiveOne"
        form = {
            "liveId": str(liveId)
        }
        try:
            response = requests.post(
                url, json=form, headers=self.headers).json()
            if response['status'] == 200:
                playStreamPath = response['content']['playStreamPath']
                return playStreamPath, response
            else:
                return False, False
        except BaseException:
            return False, False

    def encrypt(self, string):
        '''
        加密
        :param string:
        :return: 加密字符串
        '''
        token = self.Fernet.encrypt(string.encode()).decode()
        return token

    def decrypt(self, token):
        '''
        解密
        :param token:
        :return: 原文
        '''
        string = self.Fernet.decrypt(token.encode()).decode()
        return string


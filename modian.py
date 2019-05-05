'''
@author: DipperStar
@mail: ssr@yinheng.xyz
'''
import hashlib
import requests
import urllib
from cqapi import CQclient
from Scheduler import SCHEDULE
from mongo import MongoDB
import time

ORDERS_MESSAGE = 'ID: "%s" 的聚聚刚刚在 "%s" 中支持了 ¥%s\n当前集资进度：¥%s\n目标：¥%s\n链接：%s'
RANK_MESSAGE = '#{}\t{}\t¥{}\n' * 20
DETAIL_MESSAGE = '%s\n当前集资进度：¥%s\n参与人数：%s\n目标：¥%s\n%s\n链接：%s'


class MODIAN(CQclient, SCHEDULE):
    def __init__(self, pro_id):
        '''
        :param pro_id: 众筹项目编号 int
        '''
        super().__init__()
        SCHEDULE.__init__(self)
        self.pro_id = pro_id
        self.url = 'https://zhongchou.modian.com/item/' + str(self.pro_id)
        self.dbmodian = MongoDB('modian', str(self.pro_id))
        # self.dbmodian.remove({})
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        self.url = 'https://m.modian.com/project/' + str(self.pro_id)
        self.dataType = dict(orders=ORDERS_MESSAGE, rank=RANK_MESSAGE,
                             detail=DETAIL_MESSAGE)

    @property
    def update_data(self):
        '''
        上传数据到数据库，返回新增数据
        :return: 新增数据 list
        '''
        list_orders = []
        for data in self.orders(1)['data']:
            if self.dbmodian.update(data, upsert=True) == 'success':
                if data['types'] == 'orders':
                    list_orders.append(data)
        return list_orders

    def format_data(self, data):
        '''
        格式化数据格式，用于QQ发送
        :param data:
        :return: QQ消息 tuple
        '''
        if type(data) != list:
            types = data['types']
            template = self.dataType[types]
            detail = self.detail['data'][0]
            if types == 'orders':
                msg = (template % (
                data['nickname'], detail['pro_name'], data['backer_money'], detail['already_raised'], detail['goal'],
                self.url))
            elif types == 'detail':
                msg = (template % (detail['pro_name'], detail['already_raised'], detail['backer_count'], detail['goal'],
                                   detail['left_time'], self.url))
        else:
            temp = []
            template = self.dataType[data[0]['types']]
            for k in data:
                temp.append(k['rank'])
                temp.append(k['nickname'])
                temp.append(k['backer_money'])
            msg = (template.format(*temp))
        return msg

    def sign(self, ret):
        '''
        生成签名，用于post传参
        :param ret: form json
        :return: sign string
        '''
        tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
        md5_string = urllib.parse.urlencode(tuple).encode(encoding='utf_8', errors='strict')
        md5_string += b'&p=das41aq6'
        sign = hashlib.md5(md5_string).hexdigest()[5: 21]
        return sign

    def orders(self, page, sort_by=1):
        '''
        获取订单详情
        :param page: 页码 int
        :param sort_by: 排序方式 1：支付时间倒序 0：下单时间倒序 int
        :return: 订单列表详情 json
        '''
        url = 'https://wds.modian.com/api/project/sorted_orders'
        form = {
            'page': page,
            'pro_id': self.pro_id,
            'sort_by': sort_by
        }
        form['sign'] = self.sign(form)
        response = requests.post(url, form, headers=self.headers, timeout=5).json()
        for data in response['data']:
            data.update({'types': 'orders'})
        return response

    def rank(self, type, page):
        '''
        获取众筹排行榜
        :param type: 排行榜类型 1：金额榜 2：打卡榜 int
        :param page: 页码 int
        :return: 排行榜详情 json
        '''
        url = 'https://wds.modian.com/api/project/rankings'
        form = {
            'page': page,
            'pro_id': self.pro_id,
            'type': type
        }
        form['sign'] = self.sign(form)
        response = requests.post(url, form, headers=self.headers, timeout=5).json()
        for data in response['data']:
            data.update({'types': 'rank'})
        return response

    @property
    def detail(self):
        '''
        获取众筹项目详情
        :return: 项目详情 json
        '''
        url = 'https://wds.modian.com/api/project/detail'
        form = {
            'pro_id': self.pro_id
        }
        form['sign'] = self.sign(form)
        response = requests.post(url, form, headers=self.headers, timeout=5).json()
        for data in response['data']:
            data.update({'types': 'detail'})
        return response

    def _todo(self):
        '''
        发送格式化后的消息到酷Q，间隔1秒
        :return: 0
        '''
        for data in self.update_data:
            msg = self.format_data(data)
            self.single_msg(msg)
            time.sleep(1)

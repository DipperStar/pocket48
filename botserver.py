'''
@author: DipperStar
@mail: ssr@yinheng.xyz

开启机器人服务器
'''
from cqhttp import CQHttp
bot = CQHttp(api_root='http://127.0.0.1:5700/')
bot.run(host='127.0.0.1', port=8080)
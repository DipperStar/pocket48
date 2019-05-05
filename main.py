'''
@author: DipperStar
@mail: ssr@yinheng.xyz
'''
from modian import MODIAN
from pocket48 import POCKET48

modian = MODIAN(56981)
# 初始化摩点监控
modian.interval_time = 30
# 设置循环时间
tomato = POCKET48(urs, psw, '方琪')
# 初始化口袋房间监控
modian.interval_time = 120
miffy = POCKET48(urs, psw, '刘力菲')
modian.interval_time = 120
tomato.run()
miffy.run()
modian.run()
bot = modian.bot


@bot.on_message()
def call(context):
    '''
    事件处理
    :param context: 消息内容 json
    :return: 0
    '''
    if context['message'] == '$detail':
        detail_data = modian.detail['data'][0]
        msg = modian.format_data(detail_data)
        bot.send(context, msg)
    if context['message'] == '$rank':
        rank_data = modian.rank(1, 1)['data']
        msg = modian.format_data(rank_data)
        bot.send(context, msg)


bot.run(host='127.0.0.1', port=8080)
# 事件处理服务器

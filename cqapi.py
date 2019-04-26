from cqhttp import CQHttp


class CQclient(object):
    '''
    酷Q机器人
    : func single_msg: 发送私聊信息
    : func group_msg: 发送群聊信息
    : param single_id: 私聊QQ号 list
    : param group_id: 群聊QQ号 list
    '''

    def __init__(self):
        self.bot = CQHttp(api_root='http://127.0.0.1:5700/')
        self.single_id = [526189921]
        self.group_id = []

    def single_msg(self, msg):
        '''
        发送私聊信息
        : param msg: 需要发送的信息 string
        : return: 发送结果 list
        '''
        try:
            return [
                self.bot.send_private_msg(
                    message=msg,
                    user_id=_id,
                    auto_escape=False) for _id in self.single_id]
        except BaseException:
            print(msg)

    def group_msg(self, msg):
        '''
        发送群聊信息
        : param msg: 需要发送的信息 string
        : return: 发送结果 list
        '''
        try:
            return [
                self.bot.send_group_msg(
                    message=msg,
                    group_id=_id,
                    auto_escape=False) for _id in self.group_id]
        except BaseException:
            print(msg)
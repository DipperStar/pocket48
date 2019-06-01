from flask import Flask, jsonify, request
from flask_cors import CORS
from pocketapi import API
import time

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

dic_color = {}
pocket = API()


@app.route('/cheak', methods=['POST'])
def cheak():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        token = data.get('token', 'notoken')
        hastoken = pocket.token(token)
        if not hastoken:
            response_object['status'] = False
        else:
            response_object.update(hastoken)
    return jsonify(response_object)


@app.route('/login', methods=['POST'])
def login():
    '''
    登录
    :return: token及附带的信息 response_object json
    '''
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        phone = post_data.get('phone')
        password = post_data.get('password')
        res = pocket.login(phone, password)
        response_object.update(res)
    return jsonify(response_object)


@app.route('/addmember', methods=['POST'])
def addmember():
    '''
    添加成员
    :return: token及附带的信息 response_object json
    '''
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        name = post_data.get('name')
        token = post_data.get('token')
        res = pocket.addmember(name, token)
        response_object.update(res)
    return jsonify(response_object)


@app.route('/removemember', methods=['POST'])
def removemember():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        roomId = post_data.get('roomId')
        token = post_data.get('token')
        res = pocket.removemember(roomId, token)
        response_object['message'] = '删除成员成功！'
    response_object.update(res)
    return jsonify(response_object)


@app.route('/removetoken', methods=['POST'])
def removetoken():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        token = post_data.get('token')
        pocket.removetoken(token)
        response_object['message'] = '删除token成功！'
    return jsonify(response_object)


@app.route('/chat', methods=['POST'])
def chat():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        false = False
        true = True
        return_data = []
        token = request.get_json()['token']
        for dicts in pocket.chatroom(token):
            temp = dicts['res']
            color = dicts['color']
            for data in temp:
                data['extInfo'] = eval(data['extInfo'])
                times = time.strftime("%y-%m-%d %H:%M:%S", time.localtime(float(data['msgTime'] / 1000)))
                name = data['extInfo']['user']['nickName']
                try:
                    names = name.split('-')[1]
                except:
                    names = name
                avatar = 'https://source.48.cn' + data['extInfo']['user']['avatar']
                if data['msgType'] == 'TEXT':
                    types = data['extInfo']['messageType']
                    if types == 'TEXT':
                        mesg = data['bodys']
                    elif types == 'REPLY':
                        mesg = '%s：%s<br/>%s: %s' % (
                            data['extInfo']['replyName'], data['extInfo']['replyText'], name, data['bodys']
                        )
                    elif types == 'FLIPCARD':
                        mesg = '%s<br/>%s：%s' % (
                            data['extInfo']['question'], data['extInfo']['user']['nickName'], data['extInfo']['answer']
                        )
                    elif types == 'LIVEPUSH':
                        liveId = data['extInfo']['liveId']
                        playStreamPath, playDetail = pocket.livedetail(liveId)
                        if not playStreamPath:
                            playStreamPath = '暂无'
                        mesg = '<a href="https://h5.48.cn/2019appshare/memberLiveShare/index.html?id=%s">直播地址</a>' % (
                            liveId)
                elif data['msgType'] == 'IMAGE':
                    types = 'IMAGE'
                    mesg = eval(data['bodys'])['url'].replace('\/', '/')
                return_data.append(
                    {'mesg': mesg, 'time': times, 'name': names, 'color': color, 'avatar': avatar, 'type': types})
        return_data.sort(key=lambda x: x['time'], reverse=True)
        response_object['chat'] = return_data
        response_object['message'] = '请求房间消息成功！'
    return jsonify(response_object)


@app.route('/ping', methods=['GET'])
def ping():
    response_object = {'status': 'success'}
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()

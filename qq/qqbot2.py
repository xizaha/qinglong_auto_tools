# qqbot.py

# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢

client_id = [""]
client_secret = [""]
urllist = ["http://xxxxxxx:xxxx/"]
zQQ = ""

from aiocqhttp import CQHttp, Event, Message, MessageSegment
import requests, os
import time, random
import json
import re

bot = CQHttp(api_root='http://127.0.0.1:5700')  # go-cahttp部署的端口

requests.packages.urllib3.disable_warnings()
a = requests.session()


def gettimestamp():
    return str(int(time.time() * 1000))

def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})

def getckitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()
    r = self.get(url)
    for i in json.loads(r.text)["data"]:
        if key in i["value"]:
            return i
    return []

def getitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item

def gettaskitem(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item

def ckup(wskey):
    pt_key = re.findall(r"wskey=(.*?);", wskey)[0]
    pt_key = "pt_key=" + pt_key+";"
    k = re.finditer("wskey=",wskey)
    for j in k:
        t = j.span()[1]
    pt_pin = 'pt_' + wskey[0:t-7]+';'
    ck = pt_pin+pt_key+wskey.split(';')[1]+';'
    return ck

def getstatus(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/"+data[0]+"?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.get(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text

def addcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.post(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text

def runcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/run?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text

def deletecron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.delete(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text

def getlogcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/"+data[0]+"/log?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.get(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text

def push_QQ(userid, res_text, typ):
    data = {
        'user_id': userid,
        'message': res_text
    }
    requests.post('http://xxxx:xxxxx/' + typ, data)


def pre_check(userid):
    with open("data.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    Q_list = []
    p_list = []
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        p_list.append(qwe[1])
    if str(userid) in Q_list:
        b = []
        for index, nums in enumerate(Q_list):
            if nums == str(userid):
                b.append(index)
        c = []
        for j in b:
            c.append('{},{}'.format(Q_list[j], p_list[j]))
        return c
    else:
        return 'error'


def check(a, msg):
    userid = msg.split(',')[0]
    pin = msg.split(',')[1]
    #name = msg.split(',')[2]
    push_type = 'send_private_msg'


    ucount = 0
    url_token = urllist[ucount] + 'open/auth/token?client_id=' + client_id[ucount] + '&client_secret=' + client_secret[
        ucount]
    gettoken(a, url_token)
    #pin = "jd_7ac5332efb1c2"
    cks = getitem(a, urllist[0], "JD_COOKIE", "open")
    res = getitem(a, urllist[0], pin, "open")
    weizhi = cks.index(res[0]) + 1
    data = {
        "command": "task ccwav_QLScript_jd_bean_change.js conc JD_COOKIE " + str(weizhi),
        "schedule": "1",
        "name": "查询"
    }
    # 创建任务
    res1 = addcron(a, urllist[0], "open", data)
    id = json.loads(res1)["data"]["_id"]
    # print(res1)
    # 执行任务

    res2 = runcron(a, urllist[0], "open", [id])
    # print(res2)

    res3 = getstatus(a, urllist[0], "open", [id])

    while True:
        if json.loads(res3)["data"]["status"] == 0:
            msg1 = "还在查询中,请耐心等待,8秒刷新一次状态"
            push_QQ(userid, msg1, push_type)
            time.sleep(8)
            res3 = getstatus(a, urllist[0], "open", [id])
        else:
            break

    time.sleep(1)
    res4 = getlogcron(a, urllist[0], "open", [id])

    # 查询结果
    result = json.loads(res4)["data"]

    # 删除任务
    deletecron(a, urllist[0], "open", [id])

    # 发送消息
    res_text = str(result)[240:-50]
    res_text = res_text.replace("京东", "狗东")
    res_text = res_text.replace("红包", "red包")
    res_text = res_text.replace("京豆", "Jin豆")
    res_text = res_text.replace("收入", "入")

    push_QQ(userid, res_text, push_type)


def select_(chat):
    cht = chat.split(',')
    if not os.path.exists('data.txt'):
        with open("data.txt", "w") as f:
            f.write("QQ,pin,zhuanghu")
    with open("data.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    Q_list = []
    p_list = []
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        p_list.append(qwe[1])
    if cht[1] in p_list:
        return '该京东账号的pin已经被绑定了，请更换绑定账号'
    else:
        with open("data.txt", "a") as fe:
            fe.write("\n{},{}".format(cht[0], cht[1]))
        return '{},{}'.format(cht[0], cht[1])

def command_t(name):
    ucount = 0
    url_token = urllist[ucount] + 'open/auth/token?client_id=' + client_id[ucount] + '&client_secret=' +client_secret[ucount]
    gettoken(a, url_token)
    ztasks = gettaskitem(a, urllist[0], "open")
    disable_list = []
    for i in ztasks:
        if i['isDisabled'] != 0:
            disable_list.append(i)
    disable_tlid = []
    disable_tname = []
    disable_tcommand = []
    for j in disable_list:
        disable_tlid.append(j['_id'])
        disable_tname.append(j['name'])
        disable_tcommand.append(j['command'])
    count=0
    for i in disable_tname:
        if i == name:
            id = disable_tlid[count]
        count +=1
    res2 = runcron(a, urllist[0], "open", [id])
    res3 = getstatus(a, urllist[0], "open", [id])
    ms = "还在运行中，请稍后"
    push_QQ(zQQ,ms,'send_private_msg')
    while True:
        if json.loads(res3)["data"]["status"] == 0:
            time.sleep(8)
            res3 = getstatus(a, urllist[0], "open", [id])
        else:
            break
    time.sleep(1)
    res4 = getlogcron(a, urllist[0], "open", [id])
    ms = json.loads(res4)["data"][-100:-40]
    return ms

@bot.on_message
async def handle_msg(event):
    ms = Message(event.message)
    msg = str(ms)
    if msg == 'start':
        sm = '请按照提示操作\n增加QQ绑定   请以‘英文输入法’输入：\nQQ账号,京东的pin值\n格式例子：\n111111111,jd_xxxxxxx\n查询   请输入‘check’\n查询结果显示api错误不用管，只是查不到过期京豆而已'
        await bot.send(event, sm)
    elif len(msg.split(',')) == 2:
        await bot.send(event, 'QQ绑定的账号增加中')
        response = select_(msg)
        if len(response.split(',')) == 2:
            await bot.send(event, '账号增加完毕，查询资产请输入‘check’')
        else:
            await bot.send(event, response)
    elif msg == 'common' and str(event['sender']['user_id']) == zQQ:
        ms = command_t("通用开卡[普通]")
        push_QQ(zQQ,ms,'send_private_msg')
    elif msg == 'game' and str(event['sender']['user_id']) == zQQ:
        ms = command_t("通用京东游戏")
        push_QQ(zQQ,ms,'send_private_msg')
    elif msg == 'collect' and str(event['sender']['user_id']) == zQQ:
        ms = command_t("通用集卡")
        push_QQ(zQQ,ms,'send_private_msg')
    elif msg == '1600' and str(event['sender']['user_id']) == zQQ:
        ms = command_t("通用开卡[1600]")
        push_QQ(zQQ,ms,'send_private_msg')
    elif msg == 'video' and str(event['sender']['user_id']) == zQQ:
        ms = command_t("通用京东视频狂得京豆")
        push_QQ(zQQ,ms,'send_private_msg')
    elif msg == 'share' and str(event['sender']['user_id']) == zQQ:
        ms = command_t("通用分享")
        push_QQ(zQQ,ms,'send_private_msg')
    elif msg == 'check':
        await bot.send(event, '查询中')
        userid = event['sender']['user_id']
        response = pre_check(userid)
        if response == 'error':
            await bot.send(event, '查询失败')
        else:
            for i in response:
                rest = check(a, i)
    elif (msg[0] == 'p'):
        print('ck  ')
        ck = ckup(msg)
        push_QQ(zQQ,ck,'send_private_msg')
        print(ck)
    else:
        await bot.send(event, '命令输入错误，请输入‘start’仔细查看命令指南')
    await bot.send(event, '上述命令执行完毕，休息中')


bot.run(host='127.0.0.1', port=5701)  # go-cahttp监听的端口


# qqbot.py

# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢

client_id = ["h_HtkSv1fvPz"]
client_secret = ["5ZpUKsHYhmJiv-Rfi36aBX__"]
urllist = ["http://43.132.171.233:5806/"]
#tgAPI='1958551951:AAEGx2og7qjM09T7xSRXlHdvPazaAV__30g'

from aiocqhttp import CQHttp, Event, Message, MessageSegment
import requests, os
import time, random
import json
import re

bot = CQHttp(api_root='http://81.70.76.127:5700/')  # go-cahttp部署的端口

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

'''
def getlogs(self, baseurl, typ):
    url = baseurl + typ + "/logs"
    r = self.get(url)
    res = json.loads(r.text)["dirs"]
    return res


def getfiles(dirs, name):
    for i in dirs:
        if i['name'] == name:
            return i['files']
    return []


def getdetail(self, baseurl, files, filename):
    url = baseurl + "open/logs/" + files + '/' + filename + '/'
    r = a.get(url)
    return r.text
'''

def ckup(wskey):
    #wskey=input("请输入wskey（样例：pin=xxxxxxx;wskey=xxxxx）：")
    ws=wskey
    headers = {
            "Host": "signer.nz.lu",
            "user-agent": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
    url="http://cdn.xia.me/getck"
    data={"wskey": ws ,"key":"xb3z4z2m3n847"}
    data=json.dumps(data)
    r=requests.post(url,headers=headers,data=data, verify=False)
    i = str(r.text)
    pt_key = i[0:90]+';'
    k = re.finditer("wskey=",ws)
    for j in k:
        t = j.span()[1]
    pt_pin = 'pt_' + ws[0:t-7]+';'
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
    requests.post('http://81.70.76.127:5700/' + typ, data)


def pre_check(userid):
    with open("data.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    Q_list = []
    p_list = []
    #z_list = []
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        p_list.append(qwe[1])
        #z_list.append(qwe[2])
    if str(userid) in Q_list:
        b = []
        for index, nums in enumerate(Q_list):
            if nums == str(userid):
                b.append(index)
        c = []
        for j in b:
            c.append('{},{}'.format(Q_list[j], p_list[j]))#, z_list[j]))
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
            msg1 = "还在查询中，请耐心等待"
            push_QQ(userid, msg1, push_type)
            time.sleep(3)
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
    res_text = pin + '查询的资产，定时每日12点更新当天资产\n' + result
    res_text = res_text.replace("京东", "狗东")
    res_text = res_text.replace("红包", "red包")
    res_text = res_text.replace("京豆", "Jin豆")
    res_text = res_text.replace("收入", "入")

    push_QQ(userid, res_text, push_type)
    return res_text


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
    z_list = []
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        p_list.append(qwe[1])
        z_list.append(qwe[2])
    if cht[1] in p_list:
        # index = p_list.index(cht[1])
        # return '{},{},{}'.format(Q_list[index],p_list[index],z_list[index])
        return '该京东账号的pin已经被绑定了，请更换绑定账号'
    else:
        with open("data.txt", "a") as fe:
            fe.write("\n{},{},{}".format(cht[0], cht[1], cht[2]))
        return '{},{},{}'.format(cht[0], cht[1], cht[2])

'''
def tg_select(chat):
    cht = chat.split(',')
    if not os.path.exists('tg.txt'):
        with open("tg.txt", "w") as f:
            f.write("QQ,tg")
    with open("tg.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    Q_list = []
    tg_list = []
    for i in tmpss:
        tp = i.split(',')
        Q_list.append(tp[0])
        tg_list.append(tp[1])
    if cht[0] in Q_list:
        return '该QQ账号的tg已经被绑定了，请更换QQ账号'
    else:
        with open("tg.txt", "a") as fe:
            fe.write("\n{},{}".format(cht[0], cht[1]))
        return "{},{}".format(cht[0], cht[1])


def tg_check_(cht):
    with open("tg.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    Q_list = []
    tg_list = []
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        tg_list.append(qwe[1])
    if cht in Q_list:
        index = Q_list.index(cht)
        return tg_list[index]
    else:
        return 'error'


def tgpush_(tg_id, res, tgAPI):
    # 国内机子
    push_url = 'https://cloudfare代理的api端口/bot' + tgAPI + '/sendMessage'
    # 国外机子这里的api是直接使用api.telegram.org即可
    data = {
        'chat_id': tg_id,
        'text': res
    }
    requests.post(push_url, data=data)
'''

@bot.on_message
async def handle_msg(event):
    ms = Message(event.message)
    msg = str(ms)
    if msg == 'start':
        sm = '请按照提示操作\n增加QQ绑定   请以‘英文输入法’输入：\nQQ账号,京东的pin值\n格式例子：\n111111111,jd_xxxxxxx\n查询   请输入‘check’\nQQ若有绑定tg，查询时qq和tg一起发消息给你\n查询结果显示api错误不用管，只是查不到过期京豆而已'
        await bot.send(event, sm)
    elif len(msg.split(',')) == 2:
        await bot.send(event, 'QQ绑定的账号增加中')
        response = select_(msg)
        if len(response.split(',')) == 2:
            await bot.send(event, '账号增加完毕，查询资产请输入‘check’')
        else:
            await bot.send(event, response)
    elif msg == 'check':
        await bot.send(event, '查询中')
        userid = event['sender']['user_id']
        #tg_data = tg_check_(str(userid))
        #if tg_data == 'error':
        #    print('tg push error')
        #else:
        #    tg_id = tg_data
        response = pre_check(userid)
        if response == 'error':
            await bot.send(event, '查询失败')
        else:
            for i in response:
                rest = check(a, i)
                #tgpush_(tg_id, rest, tgAPI)
                await bot.send(event, str(rest))
    else:
        await bot.send(event, '命令输入错误，请输入‘start’仔细查看命令指南')
    await bot.send(event, '上述命令执行完毕，休息中')


bot.run(host='81.70.76.127', port=5701)  # go-cahttp监听的端口



'''
    elif len(msg.split(',')) == 2:
        await bot.send(event, 'QQ绑定的TG账号增加中')
        restg = tg_select(msg)
        if len(restg.split(',')) == 2:
            await bot.send(event, 'TG绑定完毕，查询资产请输入‘check’')
        else:
            await bot.send(event, restg)
'''

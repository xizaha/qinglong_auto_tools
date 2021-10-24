#!/usr/bin/env python3
# -*- coding: utf-8 -*

'''
原项目名称: JD-Script / jd_ccfxj_help
原作者: Curtin
修改者: spiritlhl

说明：二叉树修改自pkc的并发版本

修改者的仓库:https://github.com/spiritLHL/qinglong_auto_tools
觉得不错麻烦点个star谢谢

原作者信息：
TG交流 https://t.me/topstyle996
TG频道 https://t.me/TopStyle2021

原作者和修改者不是同一人，有事别找我，勿喷

cron: 0 0 * * *
new Env('城城分现金-助力-二叉树修改-并发.py');
'''

# 互助码自己写，别留空，作者助力码祈求留个位置跑一次谢谢

share = ['RtGKz733RAmgfNbMRdVg1M-xhDqLnmB3Yv0gq-pzIDUo8hszTw','别留','别留']

# UA 可自定义你的，注意格式: 【 jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1 】
UserAgent = ''

import os, re, sys
import random, json, time, threading

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
from urllib.parse import unquote

# requests.packages.urllib3.disable_warnings()
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
addressid = ''.join(random.sample('1234567898647', 10))
iosVer = ''.join(random.sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
iosV = iosVer.replace('.', '_')
iPhone = ''.join(random.sample(["8", "9", "10", "11", "12", "13"], 1))
ADID = ''.join(random.sample('0987654321ABCDEF', 8)) + '-' + ''.join(
    random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(
    random.sample('0987654321ABCDEF', 4)) + '-' + ''.join(random.sample('0987654321ABCDEF', 12))
###



def thread_func():  # 线程函数
    wz = share.pop(0)
    print("\n助力：{}".format(wz))
    for ck, user in zip(cookiesList, userNameList):
        zhuli(ck, wz, user)


def many_thread():
    threads = []
    temp = share.copy()
    for _ in range(len(temp)):
        t = threading.Thread(target=thread_func)
        threads.append(t)
    for t in threads:
        t.start()


def gettimestamp():
    return str(int(time.time() * 1000))


def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})


def login(self, baseurl, cilent_id_temp, cilent_secret_temp):
    url_token = baseurl + 'open/auth/token?client_id=' + cilent_id_temp + '&client_secret=' + cilent_secret_temp
    gettoken(self, url_token)


def getitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def userAgent():
    """
    随机生成一个UA
    jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1
    :return: ua
    """
    if not UserAgent:
        return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'
    else:
        return UserAgent


## 获取通知服务
class msg(object):
    def __init__(self, m):
        self.str_msg = m
        self.message()

    def message(self):
        global msg_info
        print(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()

    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass

    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")
        ###################


msg("").main()


##############

def buid_header(ck):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://bunearth.m.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': ck,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.m.jd.com',
        'Connection': 'keep-alive',
        'User-Agent': userAgent(),
        'Referer': 'https://bunearth.m.jd.com/babelDiy/Zeus/x4pWW6pvDwW7DjxMmBbnzoub8J/index.html?inviteId=&encryptedPin=&lng=113.&lat=23.&sid=&un_area=',
        'Accept-Language': 'zh-cn'
    }
    return headers


def getInviteId(ck):
    url = 'https://api.m.jd.com/client.action'
    body = 'functionId=city_getHomeData&body={"lbsCity":"19","realLbsCity":"1601","inviteId":"","headImg":"","userName":"","taskChannel":"1"}&client=wh5&clientVersion=1.0.0&uuid=' + uuid
    resp = requests.post(url=url, headers=buid_header(ck), data=body, timeout=30).json()
    userActBaseInfo = resp['data']['result']['userActBaseInfo']
    inviteId = userActBaseInfo['inviteId']
    poolMoney = userActBaseInfo['poolMoney']
    msg(f"当前助力池：{poolMoney} 元")
    return inviteId, poolMoney


def zhuli(ck, inviteId, user):
    url = 'https://api.m.jd.com/client.action'
    body = 'functionId=city_getHomeData&body={"lbsCity":"19","realLbsCity":"1601","inviteId":"' + inviteId + '","headImg":"","userName":"","taskChannel":"1"}&client=wh5&clientVersion=1.0.0&uuid=' + uuid
    resp = requests.post(url=url, headers=buid_header(ck), data=body, timeout=30).json()
    try:
        m = resp['data']['result']['toasts'][0]['msg']
        print(f"{user}--{m}")
    except:
        print(f"{user}--助力失败")


def start():
    scriptName = '### 城城分现金-助力 ###'
    print(scriptName)
    ql_new = '/ql/config/env.sh'
    ckfile = ql_new
    if os.path.exists(ckfile):
        with open(ckfile, "r", encoding="utf-8") as f:
            ckss = f.read()
            f.close()
        cookies = re.findall(r"JD_COOKIE=\"(.*?)\"", ckss)[0]
        cks = cookies.split("&")
        if len(cks) > 0:
            c_list = []
            pin_list = []
            for i in cks:
                tp = i
                ptpin = re.findall(r"pt_pin=(.*?);", tp)[0]
                ptpin = "pt_pin=" + ptpin + ';'
                pin_list.append(ptpin)
                ptkey = re.findall(r"pt_key=(.*?);", tp)[0]
                ptkey = "pt_key=" + ptkey + ';'
                c = ptkey + ptpin
                c_list.append(c)
    else:
        print("error")

    global cookiesList, userNameList, pinNameList, ckNum
    cookiesList = c_list
    userNameList = pin_list

    #  查询互助码运行此程序，去掉下方注释
    # for ck,user in zip(cookiesList,userNameList):
    #   res = getInviteId(ck)
    #   print("{}的信息:{}".format(users,str(res)))


    print("总助力人数{}\n".format(len(c_list)))

    many_thread()

    send(scriptName, msg_info)


if __name__ == '__main__':
    start()
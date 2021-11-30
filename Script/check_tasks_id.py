#!/usr/bin/env python3
# -*- coding: utf-8 -*

# 自用查任务ID
client_id1=""
client_secret1=""
url1 = "http://xxxx:xxxx/"

import re
import time
import json

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)


requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1500))


def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})


def login(self, baseurl, client_id_temp, client_secret_temp):
    url_token = baseurl + 'open/auth/token?client_id=' + client_id_temp + '&client_secret=' + client_secret_temp
    gettoken(self, url_token)


def getitem(self, baseurl, typ):
    url = baseurl + typ + "/scripts/files?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getscript(self, baseurl, typ, filename):
    url = baseurl + typ + "/scripts/" + filename + "?t=%s" % gettimestamp()
    r = self.get(url)
    script = json.loads(r.text)["data"]
    return script


def pushscript(self, baseurl, typ, data):
    url = baseurl + typ + "/scripts?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    response = json.loads(r.text)["code"]
    if response == 500:
        data["path"] = ""
    r = self.put(url, data=json.dumps(data))
    return r.text


def getcrons(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def addcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.post(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return r.text


if __name__ == '__main__':
    # 主容器
    s = requests.session()
    login(s, url1, client_id1, client_secret1)

    # 获取主青龙任务
    print("=========== 主青龙 信息获取中 =============")
    print()
    ztasks = getcrons(s, url1, "open")
    for i in ztasks: #根据青龙任务的名字查询对应ID
        if i["name"] == "通用开卡[普通]":
            print("通用开卡[普通]ID")
            print(i["_id"])
            print()
        elif i["name"] == "通用分享":
            print("通用分享ID")
            print(i["_id"])
            print()
        elif i["name"] == "通用集卡":
            print("通用集卡ID")
            print(i["_id"])
            print()
        elif i["name"] == "通用京东视频狂得京豆":
            print("通用京东视频狂得京豆ID")
            print(i["_id"])
            print()
        elif i["name"] == "通用关注有礼":
            print("通用关注有礼ID")
            print(i["_id"])
            print()
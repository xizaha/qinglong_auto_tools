# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢


'''
cron: 1
new Env('二叉树屏蔽关键词');
'''


# 主青龙，需要屏蔽关键词的容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
'''
# ec_config.txt中填写如下设置

# 二叉树清除屏蔽词
scripts_purge_keys_cilent_id1="xxxxxxx"
scripts_purge_keys_cilent_secret1="xxxxx"
scripts_purge_keys_url1="http://xxxxxx:xxxx/"

'''

import re

try:
    with open("ec_config.txt", "r") as fp:
        t = fp.readlines()
    try:
        for i in t:
            try:
                temp = re.findall(r"scripts_purge_keys_cilent_id1=\"(.*?)\"", i)[0]
                cilent_id1 = temp
                if cilent_id1 == "":
                    print("scripts_purge_keys_cilent_id1 未填写")
            except:
                pass
    except:
        print("scripts_purge_keys_cilent_id1 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = re.findall(r"scripts_purge_keys_cilent_secret1=\"(.*?)\"", i)[0]
                cilent_secret1 = temp
                if cilent_secret1 == "":
                    print("scripts_purge_keys_cilent_secret1 未填写")
            except:
                pass
    except:
        print("scripts_purge_keys_cilent_secret1 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = re.findall(r"scripts_purge_keys_url1=\"(.*?)\"", i)[0]
                url1 = temp
                if url1 == "":
                    print("scripts_purge_keys_url1 未填写")
            except:
                pass
    except:
        print("scripts_purge_keys_url1 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")


# 主青龙，需要查找网络链接的容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
#cilent_id1 = ""
#cilent_secret1 = ""
#url1 = ""

# 屏蔽词
keys = []

# 屏蔽词也可在fake_keys.txt中按一行一行填写
try:
    with open("fake_keys.txt", "r") as fp:
        t = fp.readlines()
    for j in t:
        keys.append(j)
except:
    print("fake_keys.txt 未创建，有需要请按照注释进行操作")

for i in t:
    keys.append(i)

keys = list(set(keys))

# 屏蔽词替换成real_key的值
real_key = "www.baidu.com"

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")
import time
import json

requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1500))


def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})


def login(self, baseurl, cilent_id_temp, cilent_secret_temp):
    url_token = baseurl + 'open/auth/token?client_id=' + cilent_id_temp + '&client_secret=' + cilent_secret_temp
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
    # response = json.loads(r.text)["data"]
    return r


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
    login(s, url1, cilent_id1, cilent_secret1)

    # 获取主青龙任务
    print("=========== 主青龙 信息获取中 =============")
    print()

    # 获取主青龙的脚本名
    zscripts = getitem(s, url1, "open")
    zscripts_list = []
    for i in zscripts:
        zscripts_list.append(i["key"])
    try:
        zscripts.remove("fake_keys.txt")
    except:
        pass
    print("主青龙脚本文件数量：{}".format(len(zscripts_list)))
    print()
    print()


    print("查询结束，正在修改中")
    print()

    # 查询需要更改的脚本内容
    change_script_list = []
    change_content = []
    for i in zscripts_list:
        content = getscript(s, url1, "open", i)
        data_script = {
            "filename": i,
            "content": content,
        }
        change_content.append(content)
        change_script_list.append(data_script)

    origin_script_list = change_script_list.copy()
    origin_content = change_content.copy()

    # 替换关键词
    tp = []
    for i in origin_content:
        tpp = i
        for j in keys:
            if j in tpp:
                tpp = tpp.replace(j, real_key, 30)
        tp.append(tpp)

    # 构造请求内容
    count = 0
    change_k = []
    for k in tp:
        if change_script_list[count]["content"] != k:
            data_script = {
                "filename": change_script_list[count]["filename"],
                "content": k,
            }
            change_k.append(data_script)
        else:
            change_k.append(change_script_list[count])
        count += 1

    # 修改
    count = 0
    ct = 0
    while True:
        if count <= (len(change_script_list) - 1):
            if change_k[count] != origin_script_list[count]:
                pushscript(s, url1, "open", change_k[count])
                print("屏蔽关键字的脚本文件 {}".format(change_k[count]["filename"]))
            else:
                ct += 1
            count += 1
        else:
            break
    print()

    print("屏蔽脚本文件关键词完毕")















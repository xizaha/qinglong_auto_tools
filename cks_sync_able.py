# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢

# 根据主青龙同步到副青龙中去，脚本默认同步更新副青龙环境变量的状态和值
# 如果有环境变量在副青龙不存在需要新增，若是JD_COOKIE，请使用二叉树ck分发脚本，
# 若是其他名字的变量，本脚本第一次运行自动在副青龙新增，但需要运行第二次才能同步新增变量的启用禁用状态

'''
cron: 1
new Env('二叉树环境变量状态同步');
'''

# 在脚本管理里修改这个文件的配置，然后保存，然后禁用 二叉树环境变量状态同步 这个任务，有需要再点运行


# 主青龙，需要修改环境变量的容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
# 副青龙，被同步环境变量的容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
# 按照格式有几个写几个，没有的空的删除
'''
# ec_config.txt中填写如下设置

# 二叉树环境变量状态同步
### 主青龙
cks_sync_able_cilent_id1="xxxxxxxx"
cks_sync_able_cilent_secret1="xxxxxxxxxx"
cks_sync_able_url1="http://xxxxxxxx:xxxx/"

### 副青龙
cks_sync_able_client_ids=["",""]
cks_sync_able_client_secrets=["",""]
cks_sync_able_urllist=["http://xxxxxxxxx:xxxx/",""]

'''
# client_id1=""
# client_secret1=""
# url1 = "http://ip:端口/"
# client_ids=['','','']
# client_secrets=['','','']
# urllist = ["http://xxxx:xxxx/","",""]


import time
import json
import re
try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)


try:
    with open("ec_config.txt", "r", encoding="utf-8") as fp:
        t = fp.readlines()
    try:
        for i in t:
            try:
                temp = re.findall(r"cks_sync_able_cilent_id1=\"(.*?)\"", i)[0]
                client_id1 = temp
                if client_id1 == "":
                    print("cks_sync_able_cilent_id1 未填写")
            except:
                pass
    except:
        print("cks_sync_able_cilent_id1 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = re.findall(r"cks_sync_able_cilent_secret1=\"(.*?)\"", i)[0]
                client_secret1 = temp
                if client_secret1 == "":
                    print("cks_sync_able_cilent_secret1 未填写")
            except:
                pass
    except:
        print("cks_sync_able_cilent_secret1 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = re.findall(r"cks_sync_able_url1=\"(.*?)\"", i)[0]
                url1 = temp
                if url1 == "":
                    print("cks_sync_able_url1 未填写")
            except:
                pass
    except:
        print("cks_sync_able_url1 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")


try:
    try:
        for i in t:
            try:
                temp = "["+re.findall(r"cks_sync_able_client_ids=\[(.*?)\]", i)[0]+"]"
                try:
                    client_ids = json.loads(temp)
                except:
                    print("cks_sync_able_client_ids 填写有误")
                if client_ids == []:
                    print("cks_sync_able_client_ids 未填写")
            except:
                pass
    except:
        print("cks_sync_able_client_ids 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = "["+re.findall(r"cks_sync_able_client_secrets=\[(.*?)\]", i)[0]+"]"
                try:
                    client_secrets = json.loads(temp)
                except:
                    print("cks_sync_able_client_secrets 填写有误")
                if client_secrets == []:
                    print("cks_sync_able_client_secrets 未填写")
            except:
                pass
    except:
        print("cks_sync_able_client_secrets 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = "["+re.findall(r"cks_sync_able_urllist=\[(.*?)\]", i)[0]+"]"
                try:
                    urllist = json.loads(temp)
                except:
                    print("cks_sync_able_urllist 填写有误")
                if urllist == []:
                    print("cks_sync_able_urllist 未填写")
            except:
                pass
    except:
        print("cks_sync_able_urllist 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")

requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1500))

def gettoken(self,url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer "+res})

def login(self, baseurl, client_id_temp, client_secret_temp):
    url_token = baseurl+'open/auth/token?client_id='+client_id_temp+'&client_secret='+client_secret_temp
    gettoken(self, url_token)

def getitem(self, baseurl, typ):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getenvitem(self, baseurl, value, typ, sm, tm):
    url = baseurl + typ + "/envs?search=%s&t=%s" % (sm ,gettimestamp())
    r = self.get(url)
    for i in json.loads(r.text)["data"]:
        if value in i[tm]:
            return i
    return []


def update(self, baseurl, typ, text, qlid, name):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = {
        "name": name,
        "value": text,
        "_id": qlid
    }
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def insert(self, baseurl, typ, text, nam):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = []
    data_json = {
        "value": text,
        "name": nam
    }
    data.append(data_json)
    r = self.post(url, json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def enable(self, baseurl, typ, ids):
    url = baseurl + typ + "/envs/enable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(ids))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False

def disable(self, baseurl, typ, ids):
    url = baseurl + typ + "/envs/disable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(ids))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    # 不需要新增值的环境变量名
    except_list = ["JD_COOKIE"]

    #主容器
    s = requests.session()
    login(s, url1, client_id1, client_secret1)

    #获取主青龙信息
    print("=========== 主青龙 环境变量信息获取中 =============")

    env_data = getitem(s, url1, "open")
    enable_values = []
    enable_names = []
    disable_values = []
    disable_names = []
    env_values = []
    env_names = []
    for i in env_data:
        if i['status'] == 1:
            disable_values.append(i['value'])
            disable_names.append(i['name'])
        else:
            enable_values.append(i["value"])
            enable_names.append(i['name'])
        env_values.append(i["value"])
        env_names.append(i['name'])

    print("环境变量启用：{}  禁用：{}".format(len(enable_values), len(disable_values)))
    print("=========== 主青龙环境变量获取完毕 =============")

    print()
    print("脚本默认同步更新副青龙环境变量的状态和值")
    print("有环境变量在副青龙不存在需要新增，若是JD_COOKIE，请使用二叉树ck分发脚本，若是其他名字的变量，本脚本自动新增，但需要运行第二次才能同步新增变量的启用禁用状态")
    print()




    ucount = 0
    for rrr in urllist:
        print("=========== 副青龙{} 环境变量信息获取中 =============".format(ucount + 1))
        print()
        a = requests.session()
        url_token = urllist[ucount] + 'open/auth/token?client_id=' + client_ids[ucount] + '&client_secret=' + \
                    client_secrets[
                        ucount]
        gettoken(a, url_token)
        fenv_data = getitem(a, urllist[ucount], "open")
        fenv_values = []
        fenable_values = []
        fenable_names = []
        fdisable_values = []
        fdisable_names = []
        for i in fenv_data:
            if i['status'] == 1:
                fdisable_values.append(i['value'])
                fdisable_names.append(i['name'])
            else:
                fenable_values.append(i["value"])
                fenable_names.append(i['name'])
            fenv_values.append(i['value'])

        print("环境变量启用：{}  禁用：{}".format(len(fenable_values), len(fdisable_values)))
        print()


        # 更新环境变量
        print("更新环境变量值中")
        print()
        co = 0
        for k in env_values:
            name = env_names[co]
            co += 1
            if name not in except_list:
                item = getenvitem(a, urllist[ucount], name, "open", name, "name")
                if item != []:
                    qlid = item["_id"]
                    if update(a, urllist[ucount], "open", k, qlid, name):
                        print("第%s个环境变量更新成功" % (co))
                    else:
                        print("第%s个环境变量更新失败" % (co))
                else:
                    if insert(a, urllist[ucount], "open", k, name):
                        print("第%s个环境变量添加成功" % co)
                    else:
                        print("第%s个环境变量添加失败" % co)
            elif name == "JD_COOKIE":
                ptpin = re.findall(r"pt_pin=(.*?);", k)[0]
                ptpin = "pt_pin=" + ptpin
                item = getenvitem(a, urllist[ucount], ptpin, "open", k, "value")
                if item != []:
                    qlid = item["_id"]
                    if update(a, urllist[ucount], "open", k, qlid, name):
                        continue
                else:
                    continue

            else:
                print("无法识别{}".format(name))

        print()




        print("环境变量值更新完毕")
        print()


        # 同步启用环境变量
        co = 0
        enable_ids = []
        for k in enable_values:
            name = enable_names[co]
            co += 1
            if name not in except_list and k in fenv_values:
                item = getenvitem(a, urllist[ucount], k, "open", name, "value")
            elif name == "JD_COOKIE" and k in fenv_values:
                ptpin = re.findall(r"pt_pin=(.*?);", k)[0]  # 默认获取的变量里的pt_pin=xxx;里的xxx
                item = getenvitem(a, urllist[ucount], ptpin, "open", k, "value")
            else:
                continue
            enable_ids.append(item["_id"])
        enable(a, urllist[ucount], "open", enable_ids)
        print("环境变量状态更新启用完毕")
        print()


        # 同步禁用变量

        co = 0
        disable_ids = []
        for k in disable_values:
            name = disable_names[co]
            co += 1
            if name not in except_list and k in fenv_values:
                item = getenvitem(a, urllist[ucount], k, "open", name, "value")
            elif name == "JD_COOKIE" and k in fenv_values:
                ptpin = re.findall(r"pt_pin=(.*?);", k)[0]  # 默认获取的变量里的pt_pin=xxx;里的xxx
                item = getenvitem(a, urllist[ucount], ptpin, "open", k, "value")
            else:
                continue
            disable_ids.append(item["_id"])
        disable(a, urllist[ucount], "open", disable_ids)

        print("环境变量状态更新禁用完毕")
        print()

        ucount += 1
        print("=========== 副青龙%s更新环境变量完毕 ===========" % ucount)
        print()


    print("所有环境变量同步更新完毕")
















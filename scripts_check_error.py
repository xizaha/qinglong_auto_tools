# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('二叉树监控脚本运行');
'''
import random
import requests
import time
import json
import os

# 该脚本将启用的任务对应的日志进行检索
# 若脚本日志异常，分类成6大异常，并输出异常的任务名字
# 自动禁用只会自动禁用含 结束的活动 的关键词的任务日志对应的任务
# 有别的类别的自动禁用需求，自行更改本脚本219行

errr_text = [
    "Response code",
    "Error: Cannot find module",
    "异常",
    "操作太频繁",
    "TypeError: Cannot read property",
    "活动已经结束",
    "活动太火爆",
    "点太快"
]

ql_auth_path = '/ql/config/auth.json'

print("该脚本将启用的任务对应的日志进行检索，若脚本日志异常，分类成6大异常，并输出异常的任务名字，自动禁用只会自动禁用含 结束的活动 的任务，有别的类别的自动禁用需求，自行更改本脚本219行，详细更改方法看脚本注释\n")

try:
    if os.environ["ec_log_disable"] == "true":
        ec_log_disable = True
        print("已配置自动禁用含 结束的活动 的任务\n")
    else:
        pass
except:
    ec_log_disable = False
    print("默认不禁用任务")
    print("请在配置文件中配置 export ec_log_disable=\"true\" 开启脚本自动禁用任务\n")

requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1500))


def __get_token() -> str or None:
    with open(ql_auth_path, 'r', encoding='utf-8') as f:
        j_data = json.load(f)
    return j_data.get('token')


def gettoken(self):
    res = __get_token()
    self.headers.update({"Authorization": "Bearer " + res})


def login(self):
    gettoken(self)


def getitem(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getenvs(self, baseurl, typ):
    url = baseurl + typ + "/envs"
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getlogcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/" + data[0] + "/log?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.get(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text


def synchronous_tasks_disable(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/disable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return r.text


def getcrons(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


if __name__ == '__main__':
    print("===================================")
    print("查询任务日志中")

    print("--------------------------------")
    s = requests.session()
    login(s)
    try:
        ql_url = 'http://localhost:5700/'
        ztasks = getitem(s, ql_url, "api")
    except:
        ql_url = 'http://localhost:5600/'
        ztasks = getitem(s, ql_url, "api")
    enable_list = []
    for i in ztasks:
        if i['isDisabled'] == 0:
            if i["command"][-2:] == "js" or i["command"][-2:] == "py":
                enable_list.append(i)
    pf = []  # 频繁
    hb = []  # 火爆
    js = []  # 结束
    yl = []  # 依赖
    wl = []  # 网络
    zx = []  # 执行
    for i in enable_list:
        # script_name = i["command"].replace("task ", "").split("/")[0]
        try:
            res = getlogcron(s, ql_url, "api", [i["_id"]])
            status = 0

            for j in errr_text:
                if j in res:
                    status = 1
            if status == 1:
                # print("{}".format(i["name"]))
                # print("已知报错原因:")

                if "操作太频繁" in res or "点太快" in res:
                    pf.append(i)
                    # print("操作太频繁")

                if "活动太火爆" in res:
                    hb.append(i)
                    # print("活动太火爆")

                if "活动已经结束" in res:
                    js.append(i)
                    # print("活动已经结束")

                if "Error: Cannot find module" in res:
                    yl.append(i)
                    # print("找不到模块，可能缺少依赖文件或依赖环境")

                if "Response code" in res:
                    wl.append(i)
                    # print("网络原因的错误导致上报状态码")

                if "TypeError: Cannot read property" in res:
                    zx.append(i)
                    # print("执行过程中有 报错 ，未知原因")

                if "异常" in res:
                    zx.append(i)
                    # print("执行过程中有 异常 ，未知原因")

                # print("--------------------------------")
                time.sleep(random.uniform(0.2, 0.5))
            else:
                pass
        except:
            print("{}查不到日志".format(i["name"]))

    print("启用的任务对应的日志中存在错误的任务名字为：")
    print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
    print("操作太频繁:")
    for k in [j["name"] for j in pf]:
        print(k)

    print()
    print("活动太火爆:")
    for k in [j["name"] for j in hb]:
        print(k)

    print()
    print("活动已经结束:")
    for k in [j["name"] for j in js]:
        print(k)

    print()
    print("缺少依赖:")
    for k in [j["name"] for j in yl]:
        print(k)

    print()
    print("网络请求问题:")
    for k in [j["name"] for j in wl]:
        print(k)

    print()
    print("执行过程中有问题:")
    for k in [j["name"] for j in zx]:
        print(k)
    print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")

    if ec_log_disable == True:
        print("已配置自动禁用任务")
        temp = []
        # 六大类别
        # pf  点击频繁
        # hb  活动火爆
        # js  活动结束
        # yl  缺少依赖
        # wl  网络问题
        # zx  执行异常
        temp = temp + js  # 有需求自己改这行自行添加需要禁用的任务类别往后 +hb+zx 这样子写
        tp = []
        for j in temp:
            if j not in tp:
                tp.append(j)
        disable_list_log = []
        for k in tp:
            disable_list_log.append(k["_id"])
            print("自动禁用任务： {}".format(k["name"]))
        synchronous_tasks_disable(s, ql_url, "api", disable_list_log)
    else:
        print("未配置自动禁用任务")
        print("请在配置文件中配置 export ec_log_disable=\"true\" 开启脚本自动禁用任务\n")
    print("===================================")
















# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('单容器 二叉树后置黑号');
'''

# 谨慎配置！！！自测无问题但实际运行可能有bug！！！可能会打乱原有环境变量顺序！！！
# 禁用的ck自动后置，检索任务对应日志标注黑号后自动后置
# 默认任务定时自行修改

print("谨慎配置！！！自测无问题但实际运行可能有bug！！！可能会打乱原有环境变量顺序！！！")

import os
import time
import json
import re
import random

print(
    "查询的模板，黑号上方显示pin那一行的需要给出来，下方是日志以及对应需要填写的东西(xx_XXXXX是pin)\n\n\n==========检索的模板任务日志👇=========\n*********【账号 10】jd_EMgmYJMyrMHn*********\n黑号！\n*********【账号 11】jd_LjfgropqstnG*********\n黑号！\n==============模板日志👆=============\n\n此时需要的配置如下\n")

print("export ec_remode=\"】(.*?)\*\*\*\*\*\*\*\*\*)\"\nexport ec_blackkey=\"黑号！\"\nexport ec_check_task_name=\"青龙中任务的中文名字\"export ec_rear_back_ck=\"true\"\n")

print("配置中填完后就能运行脚本自动检索对应任务名字下的日志查询黑号标注黑号后置黑号了")

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

print("=================正式开始运行脚本，上述文字只是说明=========================")

try:
    os.environ["ec_check_task_name"]
except:
    os.environ["ec_check_task_name"] = ""

try:
    if os.environ["ec_check_task_name"] != "":
        check_task_name = os.environ["ec_check_task_name"]
        print("已配置开启日志检索标注黑号，检索日志任务名字为:\n{}\n".format(check_task_name))
    else:
        check_task_name = ""
        print("未配置日志检索标注黑号")
        pass
except:
    print("默认不开启日志检索标注黑号")
    print("有需要请在配置文件中配置\nexport ec_check_task_name=\"任务名字\"\n开启标注")
    print("开启标注后将检索日志中的黑号进行标注，但不会自动后置\n")
    check_task_name = ""

try:
    os.environ["ec_remode"]
except:
    remode = r"】(.*?)\*\*\*\*\*\*\*\*\*"
    pass

try:
    if os.environ["ec_remode"] != "】(.*?)\*\*\*\*\*\*\*\*\*" and os.environ["ec_check_task_name"] != "":
        remode = os.environ["ec_remode"]
        print("已配置自定义re模板\n")
    else:
        print("未配置自定义re模板")
        pass
except:
    if os.environ["ec_check_task_name"] != "":
        print("使用默认模板")
        print("有需要请在配置文件中配置\n export ec_remode=\"re模板\" 自定义模板")


try:
    os.environ["ec_blackkey"]
except:
    ec_blackkey = "黑号"
    pass

try:
    if os.environ["ec_blackkey"] != "黑号" and os.environ["ec_blackkey"] != "":
        ec_blackkey = os.environ["ec_blackkey"]
        print("已配置自定义黑号关键词\n")
    else:
        print("未配置自定义黑号关键词，使用默认关键词：黑号")
        pass
except:
    try:
        os.environ["ec_blackkey"]
    except:
        ec_blackkey = "黑号"
        print("使用默认黑号关键词：黑号")
        print("有需要请在配置文件中配置\n export ec_blackkey=\"黑号关键词\" 自定义黑号关键词")



try:
    head = int(os.environ["ec_head_cks"])
    print("已配置保留前{}位ck不检索是否黑号".format(head))
except:
    head = 6
    print("#默认只保留前6位不检索是否黑号，有需求")
    print("#请在配置文件中配置\nexport ec_head_cks=\"具体几个\" \n#更改不检索是否黑号的个数\n")

try:
    if os.environ["ec_rear_back_ck"] == "true":
        ec_rear_back_ck = True
        print("已配置自动后置标注的黑号\n")
    else:
        ec_rear_back_ck = False
        print("未配置自动后置标注的黑号，默认自动后置")
except:
    print("默认不后置标注的黑号")
    print("有需要请在配置文件中配置\n export ec_rear_back_ck=\"true\" 开启自动后置")
    print("开启后将自动后置标注的黑号\n")
    ec_rear_back_ck = False

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)

requests.packages.urllib3.disable_warnings()

ql_auth_path = '/ql/config/auth.json'


def __get_token() -> str or None:
    with open(ql_auth_path, 'r', encoding='utf-8') as f:
        j_data = json.load(f)
    return j_data.get('token')


def __get__headers() -> dict:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + __get_token()
    }
    return headers


# 查询环境变量
def get_envs(name: str = None) -> list:
    params = {
        't': int(time.time() * 1000)
    }
    if name is not None:
        params['searchValue'] = name
    res = requests.get(ql_url + '/api/envs', headers=__get__headers(), params=params)
    j_data = res.json()
    if j_data['code'] == 200:
        return j_data['data']
    return []


def gettimestamp():
    return str(int(time.time() * 1000))


def gettoken(self):
    self.headers.update({"Authorization": "Bearer " + __get_token()})


def login(self):
    gettoken(self)


def getallenv(self, baseurl, typ):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getckitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()  # JD_COOKIE为默认的环境变量名，该变量里的值默认含pt_pin和pt_key，其他类似默认按照下面注释改
    r = self.get(url)
    for i in json.loads(r.text)["data"]:
        if key in i["value"]:
            return i
    return []


def gettaskitem(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
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


def update(self, baseurl, typ, value, qlid, remarks):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = {
        "name": "JD_COOKIE",
        "value": value,
        "_id": qlid,
        "remarks": remarks
    }
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def move(self, baseurl, typ, id, fromIndex, toIndex):
    url = baseurl + typ + "/envs/{}/move".format(str(id))
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data_json = {
        "fromIndex": fromIndex,
        "toIndex": toIndex
    }
    params = {
        "t": int(time.time() * 1000),
        "id": str(id)
    }
    r = self.put(url, json.dumps(data_json), params=params)
    if json.loads(r.text)["code"] == 200:
        return r.json()
    else:
        return r.text


if __name__ == '__main__':
    s = requests.session()
    login(s)
    try:
        ql_url = 'http://localhost:5700/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")
    except:
        ql_url = 'http://localhost:5600/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")

    print("============================================")

        # 无配置时执行
    if os.environ["ec_check_task_name"] == "" and ec_rear_back_ck == True:
        allenv = getallenv(s, ql_url, "api")
        disable_list = []
        for i in allenv:
            if i["status"] != 0:
                disable_list.append(i)

        print("未配置检索任务名称，自动检索已有备注自动后置黑号和禁用ck\n")

        print("不检索日志只自动后置备注为“黑号”的环境变量\n")


        black_count = 0
        count = 0
        allenv = getallenv(s, ql_url, "api")
        for i in allenv:
            allenv = getallenv(s, ql_url, "api")
            try:
                i["remarks"]
                if i["remarks"] == "黑号 " or i["remarks"] == "黑号":
                    status = 1
                else:
                    status = 0
            except:
                status = 0
                pass
            count += 1
            if status == 1:
                move(s, ql_url, "api", i["_id"], count + 1, len(allenv) - 2)
                black_count += 1

        time.sleep(1)
        count = 0
        allenv = getallenv(s, ql_url, "api")
        for i in allenv:
            allenv = getallenv(s, ql_url, "api")
            if i["status"] == 1:
                move(s, ql_url, "api", i["_id"], count + 1, len(allenv) - 2)
            count += 1

        print("自动后置已有备注黑号共{}个，禁用ck共{}个\n".format(black_count, len(disable_list)))

        print("最后3~5位位置可能时有对调，小bug懒得调了\n")
        exit(3)
    else:
        print("默认不后置标注的黑号，不进行任何操作")
        print("有需要请在配置文件中配置\n export ec_rear_back_ck=\"true\" 开启自动后置")
        print("开启后将自动后置标注的黑号\n")
        pass

    # 有配置时执行

    tasks = gettaskitem(s, ql_url, "api")
    for i in tasks:
        if i["name"] == check_task_name:
            log_path = i["log_path"]
            log_id = i["_id"]
        elif check_task_name == "":
            exit(3)

    allenv = getallenv(s, ql_url, "api")
    for i in allenv:
        try:
            i["remarks"]
            if i["remarks"] == "黑号" and ec_rear_back_ck == True:
                c = update(s, ql_url, "api", i["value"], i["id"], "")
                print(c)
        except:
            pass

    log = json.loads(getlogcron(s, ql_url, "api", [log_id]))["data"]
    data = log.split("\n")
    count = 0
    interval = [0]
    for i in data:
        if ec_blackkey in i:
            interval.append(count)
        count += 1

    black_pin = []
    for i in range(0, len(interval) - 1):
        x1 = interval[i]
        x2 = interval[i + 1]
        count = 0
        data1 = []
        for j in data:
            if count >= x1 and count <= x2:
                data1.append(j)
            count += 1
        temp = []
        for j in data1:
            if re.findall(remode, j) != []:
                temp.append(j)
        pin = re.findall(remode, temp[-1])[0]
        black_pin.append(pin)

    black_dict = {}
    allenv = getallenv(s, ql_url, "api")
    count = 0 # 检索到第几个环境变量
    jdcount = 0 # 从头往后数第几个是jd_cookie
    disable_list = [] # 保存禁用的变量信息
    disable_list_count = [] # 保存位置信息
    head_env = [] # 保存头环境变量
    for i in allenv:
        if "JD_COOKIE" == i["name"] and jdcount == 0:
            jdcount = count
        if jdcount == 0 or count <= (jdcount + head):
            head_env.append(i)
        if i["status"] != 0:
            disable_list.append(i)
            disable_list_count.append(count + 1)
        for j in black_pin:
            black = "pt_pin=" + j + ";"
            if black in i["value"] and count > (jdcount + head):
                black_dict[black] = {
                    "id": i["_id"],
                    "index": count + 1,
                    "value": i["value"]
                }
        count += 1


    count = 0
    for i, j in zip(disable_list, disable_list_count):
        allenv = getallenv(s, ql_url, "api")
        if count == 0 and ec_rear_back_ck == True:
            move(s, ql_url, "api", i["_id"], j, len(allenv) - 2)
        allenv = getallenv(s, ql_url, "api")
        count = 0
        for k in allenv:
            if i["value"] == k["value"] and ec_rear_back_ck == True:
                move(s, ql_url, "api", i["_id"], count + 1, len(allenv) - 2)
            count += 1

    for i in black_dict:
        if check_task_name != "":
            update(s, ql_url, "api", black_dict[i]["value"], black_dict[i]["id"], "黑号")
            print("黑号：  {}".format(i))
        allenv = getallenv(s, ql_url, "api")
        count = 0
        for j in allenv:
            if black_dict[i]["value"] == j["value"] and ec_rear_back_ck == True:
                move(s, ql_url, "api", black_dict[i]["id"], count + 1, len(allenv) - len(disable_list) - 2)
            count += 1
        if ec_rear_back_ck == True:
            move(s, ql_url, "api", black_dict[i]["id"], black_dict[i]["index"], len(allenv) - len(disable_list))

    count = 0
    allenv = getallenv(s, ql_url, "api")
    for i in allenv:
        allenv = getallenv(s, ql_url, "api")
        try:
            i["remarks"]
            if i["remarks"] == "黑号 " or i["remarks"] == "黑号":
                status = 1
            else:
                status = 0
        except:
            status = 0
            pass
        count += 1
        if status == 1:
            move(s, ql_url, "api", i["_id"], count + 1, len(allenv) - len(disable_list))
    # 再检索防止出错
    count = 0
    allenv = getallenv(s, ql_url, "api")
    for i in allenv:
        allenv = getallenv(s, ql_url, "api")
        if i["status"] == 1:
            move(s, ql_url, "api", i["_id"], count + 1, len(allenv) - 2)
        count += 1

    # 前几个环境变量校对
    count = 0
    allenv = getallenv(s, ql_url, "api")
    for i in allenv[:(jdcount+head)]:
        if head_env[count] != i:
            move(s, ql_url, "api", i["_id"], count, jdcount+head+1)
        count += 1
        allenv = getallenv(s, ql_url, "api")


    print("最后3~5位位置可能时有对调，小bug懒得调了")

    if ec_rear_back_ck == True:
        print("\n已后置黑号共{}个".format(len(black_dict)))





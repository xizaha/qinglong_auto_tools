# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('单容器 二叉树随机ck顺序');
'''

# 初次运行生成原始顺序模板文件 trigger_cookies.json，备份原始ck文件 allck.txt
# 可每次运行重新生成模板，在配置文件中配置 export ec_write_cks="true" 开启该功能
# 默认保持前6位ck顺序不变，有需要在配置文件中配置 export ec_head_cks="具体几个" 更改数量
# 可配置随机顺序时给ck备注标上原始顺序，如果备注已存在，则保留原始备注不更改
# 禁用的ck自动后置，非ck变量全部自动前置
# 默认任务定时自行修改


import os
import time
import json
import re
import random

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)

requests.packages.urllib3.disable_warnings()

ql_auth_path = '/ql/config/auth.json'

try:
    if os.environ["ec_write_cks"] == "true":
        ec_write_cks = True
    else:
        ec_write_cks = False
        if os.path.exists("./trigger_cookies.json") == False:
            print("初次运行持久化存储原始顺序到json文件中，往后以该顺序作为模板进行随机ck排序")
            print("如果需要每次运行重新生成模板")
            print("#请在配置文件中配置\nexport ec_write_cks=\"true\" \n#开启该功能\n")
        else:
            print("已存在原始顺序模板，未配置重新生成")
            print("如果需要每次运行重新生成模板(慎重选择)")
            print("#请在配置文件中配置\nexport ec_write_cks=\"true\" \n#开启该功能\n")
except:
    ec_write_cks = False
    if os.path.exists("./trigger_cookies.json") == False:
        print("初次运行持久化存储原始顺序到json文件中，往后以该顺序作为模板进行随机ck排序")
        print("如果需要每次运行重新生成模板(慎重选择)")
        print("#请在配置文件中配置\nexport ec_write_cks=\"true\" \n#开启该功能\n")
    else:
        print("已存在原始顺序模板，未配置重新生成")
        print("如果需要每次运行重新生成模板(慎重选择)")
        print("#请在配置文件中配置\nexport ec_write_cks=\"true\" \n#开启该功能\n")

try:
    if os.environ["ec_cks_remark"] == "true":
        ec_cks_remark = True
        print("已配置备注自动填写原始顺序")
    else:
        ec_cks_remark = False
        print("未配置备注自动填写原始顺序")
        print("配置后可能会覆盖部分环境变量的备注")
        print("#请在配置文件中配置\nexport ec_cks_remark=\"true\" \n#开启该功能\n")
except:
    ec_cks_remark = False
    print("未配置备注自动填写原始顺序")
    print("配置后可能会覆盖部分环境变量的备注")
    print("#请在配置文件中配置\nexport ec_cks_remark=\"true\" \n#开启该功能\n")

try:
    head = int(os.environ["ec_head_cks"])
    print("已配置保留前{}位ck顺序做车头".format(head))
except:
    head = 6
    print("#默认只保留前6位ck做车头，有需求")
    print("#请在配置文件中配置\nexport ec_head_cks=\"具体几个\" \n#更改车头数量\n")

print("===================================")

print("已设置保留前{}位顺序不改变\n".format(head))


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


def insert(self, baseurl, typ, value, remarks=None):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = []
    data_json = {
        "value": value,
        "name": "JD_COOKIE",
        "remarks": remarks
    }
    data.append(data_json)
    r = self.post(url, json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.json()
    else:
        return r.text


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


def delete(self, baseurl, typ, value):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = value
    r = self.delete(url, data=json.dumps(data))
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
    s = requests.session()
    login(s)
    try:
        ql_url = 'http://localhost:5700/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")
    except:
        ql_url = 'http://localhost:5600/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")

    # 备份ck
    if os.path.exists("./allck.txt") == False:
        temp = []
        for i in cookies:
            temp.append(i["value"] + "\n")
        with open("./allck.txt", "w") as ffp:
            ffp.writelines(temp)
        print("初次运行，自动备份ck到allck.txt文件里，有需要恢复初始状态自取\n")
    else:
        print("脚本管理根目录下allck.txt文件已存在，有需要恢复初始状态自取\n")
        pass

    # 是否重新生成模板
    if ec_write_cks == True and os.path.exists("./trigger_cookies.json") == True:
        os.remove("./trigger_cookies.json")
    else:
        pass

    # 除ck外所有环境变量放前面
    real_list = getallenv(s, ql_url, "api")
    exc_head = 0
    for i in real_list:
        if i["name"] != "JD_COOKIE":
            exc_head += 1
            move(s, ql_url, "api", i["_id"], real_list.index(i) + 1, 1)

    print("ck前存储了{}个非ck变量\n".format(exc_head))

    ####################################################################################

    # 获取更新后的环境变量排名
    real_list = getallenv(s, ql_url, "api")
    try:
        ql_url = 'http://localhost:5700/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")
    except:
        ql_url = 'http://localhost:5600/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")

    ttpp = []
    disable_cookies = []
    for i in cookies:
        if i["status"] == 0:
            ttpp.append(i)
        else:
            disable_cookies.append(i)

    cookies = ttpp

    # 对原始顺序进行本地持久化存储
    if os.path.exists("./trigger_cookies.json") == False:
        origin_list = sorted(cookies, key=lambda x: x.__getitem__("position"), reverse=True)
        count = 1
        json_file = open("trigger_cookies.json", mode='w')
        save_json_content = []
        for i in origin_list:
            result_json = {
                "pin": re.findall(r"pt_pin=(.*?);", i["value"])[0],
                # "data": i,
                "index": count}
            save_json_content.append(result_json)
            if ec_cks_remark == True:
                update(s, ql_url, "api", i["value"], i["_id"], str(count))
            count += 1
        json.dump(save_json_content, json_file, indent=4)
        json_file.close()
        print("本地持久化存储原始顺序成功\n")

    # 随机化启用的cookie顺序，保留指定位置不变
    res = random.sample(range(exc_head + head, exc_head + len(cookies)), len(cookies) - head)
    print("固定的ck顺序")
    print("pin\t\t\t\t上次\t       本次")
    for i in range(0, head):
        c = re.findall(r"pt_pin=(.*?);", cookies[i]["value"])[0][-16:].ljust(16)
        print("{}\t\t{}\t\t{}".format(c, i + 1, i + 1))
    print("本次随机ck的顺序")
    print("pin\t\t\t\t上次\t       本次")
    temp = []
    ct = 1
    for i in res:
        temp.append(real_list[i])
        c = re.findall(r"pt_pin=(.*?);", real_list[i]["value"])[0][-16:].ljust(16)
        print("{}\t\t{}\t\t{}".format(c, i - head + 2, ct + head))
        ct += 1
    print("最后两号位置时有对换，小bug无伤大雅，懒得调了")

    time.sleep(1)

    # 进行移动操作
    ct = 1
    for i, j in zip(temp, res):
        t = real_list.index(i)
        c = move(s, ql_url, "api", i["_id"], t + 1, ct + exc_head + head)
        ct += 1

    # 禁用ck后置
    for i in disable_cookies:
        # 获取更新后的环境变量排名
        real_list = getallenv(s, ql_url, "api")

        count = 0
        for j in real_list:
            if j["value"] == i["value"] and j["name"] == i["name"]:
                count += 1
                break
            else:
                count += 1
        ct = move(s, ql_url, "api", i["_id"], count, len(real_list) - 1)

    print("\n随机ck顺序完毕，保留顺序ck共{}个，随机ck共{}个，后置禁用ck共{}个".format(head, len(temp), len(disable_cookies)))
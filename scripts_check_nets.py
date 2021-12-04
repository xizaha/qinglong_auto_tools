# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('二叉树查脚本网络链接');
'''

expect_list = ["http://xxxx.xxxx.xxx/", ""]  # 屏蔽查询的链接

import time
import json
import re
import os

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

keys = list(set(keys))

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")

requests.packages.urllib3.disable_warnings()


def traversalDir_FirstDir(path):
    list = []
    if (os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path, file)
            if (os.path.isdir(m)):
                h = os.path.split(m)
                list.append(h[1])
        return list


def read_ex(or_list):
    # 加载远程依赖剔除依赖文件的检索
    try:
        res1 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents").json()
        time.sleep(5)
        res2 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/utils").json()
        time.sleep(4)
        res3 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/function").json()
        try:
            res1["documentation_url"]
            return
        except:
            try:
                res2["documentation_url"]
                return
            except:
                try:
                    res3["documentation_url"]
                    return
                except:
                    pass


    except:
        print("网络波动，稍后尝试")
        time.sleep(5)
        try:
            res1 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents").json()
            time.sleep(5)
            res2 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/utils").json()
            time.sleep(4)
            res3 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/function").json()
            try:
                res1["documentation_url"]
                return
            except:
                try:
                    res2["documentation_url"]
                    return
                except:
                    try:
                        res3["documentation_url"]
                        return
                    except:
                        pass
        except:
            print("网络问题无法获取仓库文件列表，停止加载远程文件剔除依赖文件，直接本地检索")

    for i in res1:
        or_list.append(i["name"])
    for i in res2:
        or_list.append(i["name"])
    for i in res3:
        or_list.append(i["name"])
    or_list = list(set(or_list))
    return or_list


if __name__ == '__main__':
    # 获取主青龙任务

    print("============ 获取根目录脚本文件内容 ============\n")

    # script根目录默认存在的文件夹，放入其中的文件夹不再检索
    or_list_o = ['node_modules', '__pycache__', 'utils', '.pnpm-store', 'function', 'tools', 'backUp', '.git', '.idea',
                 'fake_keys.txt', 'ec_config.txt']
    try:
        if os.environ["ec_read_dep"] == "true":
            print("已配置远程加载依赖文件名不查询")
            or_list = read_ex(or_list_o)
            if or_list == None:
                or_list = or_list_o
    except:
        print("未配置远程加载依赖文件名不查询，有需要可添加配置")
        print("export ec_read_dep=\"true\"")
        or_list = or_list_o

    # 根目录
    dir_list = list(set(os.listdir("../") + os.listdir("./")) - set(or_list))
    data_script_list = []
    name_root = []
    if "db" not in os.listdir("../"):
        for i in dir_list:
            if i not in or_list and i[0:9] != "spiritLHL":
                try:
                    with open("../" + i, "r", encoding="utf-8") as f:
                        data_script_list.append(f.read())
                    name_root.append(i)
                except:
                    pass
    else:
        for i in dir_list:
            if i not in or_list and i[0:9] != "spiritLHL":
                try:
                    with open(i, "r", encoding="utf-8") as f:
                        data_script_list.append(f.read())
                    name_root.append(i)
                except:
                    pass

    # 筛出网址
    net_list = {}
    for i, k in zip(data_script_list, name_root):
        net_list[k] = []

    for i, k in zip(data_script_list, name_root):
        temp = re.findall(r"\"https://(.*?)\"", i)
        for j in temp:
            net_list[k].append("https://" + j)

    for i, k in zip(data_script_list, name_root):
        temp = re.findall(r"\"http://(.*?)\"", i)
        for j in temp:
            net_list[k].append("https://" + j)

    for i, k in zip(data_script_list, name_root):
        temp = re.findall(r"\'https://(.*?)\'", i)
        for j in temp:
            net_list[k].append("https://" + j)

    for i, k in zip(data_script_list, name_root):
        temp = re.findall(r"\'http://(.*?)\'", i)
        for j in temp:
            net_list[k].append("https://" + j)

    # 去重
    for i in net_list:
        net_list[i] = list(set(net_list[i]))
        for j in net_list[i]:
            if ".jd.com" in j or "." not in j or j in expect_list:
                net_list[i].remove(j)

    print()
    print("查询脚本，筛选网址中")
    print()

    # 输出找到的链接
    ## 根目录
    print("根目录文件\n")
    count_root = 0
    count_root_key = 0
    for k in net_list:
        if net_list[k] == []:
            print(k)
            print("无链接\n")
        else:
            print(k)
            for l in net_list[k]:
                print(l)
                count_root += 1
            print()
            for l in net_list[k]:
                for j in keys:
                    if j in l:
                        count_root_key += 1

    print()
    print("查到链接个数： {}".format(count_root))

    print()
    print("包含屏蔽词链接个数： {}".format(count_root_key))

    print("============ 根目录查询完毕 ============")

    ## 仓库文件待开发

    # 仓库文件夹
    # 获取副青龙仓库目录脚本名字典
    zpath_list = traversalDir_FirstDir("../")
    try:
        zpath_list.remove("spiritLHL_qinglong_auto_tools")
    except:
        pass
    if "config" not in zpath_list and "db" not in zpath_list:
        zpath_list = list(set(zpath_list) - set(or_list))
        dict_name = {}
        for i in zpath_list:
            dict_name[i] = []
            for j in list(set(os.listdir("../" + i)) - set(or_list)):
                if str(i)[0:9] != "spiritLHL":
                    dict_name[i].append(j)
    print()
    print("查询结束")














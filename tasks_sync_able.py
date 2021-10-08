#作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
#觉得不错麻烦点个star谢谢

#同步任务是否启用禁用，不存在于分容器的不会同步新增

#ql raw 拉到script里，修改script里这个文件的配置，然后添加任务设置task 新增的文件名，在你更改完主青龙后运行即可


# 主青龙，需要修改任务的容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
cilent_id1=""
cilent_secret1=""
url1 = "http://ip:端口/"

# 副青龙，被同步的任务容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
#按照格式有几个写几个，没有的空的删除
cilent_ids=['','','','']
cilent_secrets=['','','','']
urllist = ["http://xxxx:xxxx/","","",'']

import requests
import time
import json




requests.packages.urllib3.disable_warnings()
script_name = "同步任务启用禁用"

def gettimestamp():
    return str(int(time.time() * 1000))

def gettoken(self,url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer "+res})

def login(self, baseurl, cilent_id_temp, cilent_secret_temp):
    url_token = baseurl+'open/auth/token?client_id='+cilent_id_temp+'&client_secret='+cilent_secret_temp
    gettoken(self, url_token)

def getitem(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item

def synchronous_tasks_enable(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/enable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return r.text


def synchronous_tasks_disable(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/disable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8"})
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return r.text


if __name__ == '__main__':
    #主容器
    print("=========== 主容器任务状态获取中 =============")
    s = requests.session()
    login(s, url1, cilent_id1, cilent_secret1)
    ztasks = getitem(s, url1, "open")
    enable_list = []
    disable_list = []
    for i in ztasks:
        if i['isDisabled'] == 0:
            enable_list.append(i)
        else:
            disable_list.append(i)
    enable_tlid = []
    enable_tname = []
    enable_tcommand = []
    for j in enable_list:
        enable_tlid.append(j['_id'])
        enable_tname.append(j['name'])
        enable_tcommand.append(j['command'])
    disable_tlid = []
    disable_tname = []
    disable_tcommand = []
    for j in disable_list:
        disable_tlid.append(j['_id'])
        disable_tname.append(j['name'])
        disable_tcommand.append(j['command'])
    print("=======主容器任务数量：{}，启用任务{}，禁用任务{}===========".format(len(ztasks), len(enable_tname), len(disable_tname)))

    print()

    #分容器
    count = 0
    for cc in urllist:
        print("======== 分容器{}同步状态中 ============".format(count+1))
        a = requests.session()
        login(a, urllist[count], cilent_ids[count], cilent_secrets[count])
        ftasks = getitem(a, urllist[count], "open")
        tlid = []
        tname = []
        tcommand = []
        ct = 0
        for i in ftasks:
            tlid.append(i['_id'])
            tname.append(i['name'])
            tcommand.append(i['command'])

        # 启用
        enable = []
        e_name = []
        over_e = []
        for k in enable_tcommand:
            try:
                p = tcommand.index(k)
                enable.append(tlid[p])
                e_name.append(tname[p])
            except:
                p = enable_tcommand.index(k)
                over_e.append(enable_tname[p])

        # 禁用
        disable = []
        d_name = []
        over_d = []
        for k in disable_tcommand:
            try:
                p = tcommand.index(k)
                disable.append(tlid[p])
                d_name.append(tname[p])
            except:
                p = disable_tcommand.index(k)
                over_d.append(disable_tname[p])

        #同步
        synchronous_tasks_enable(a, urllist[count], 'open', enable)
        synchronous_tasks_disable(a, urllist[count], 'open', disable)

        #通知
        print('已同步状态的任务数量：{}'.format(len(e_name) + len(d_name)))
        print('分容器不存在的任务无法被同步，无法同步任务数量为：{}'.format(len(over_e) + len(over_d)))
        print("无法同步任务名如下：")
        for t in over_e:
            print(t)
        for t in over_d:
            print(t)
        count += 1
        print('========= 分容器{}同步状态完毕 ============='.format(count))
        print()

    print('同步完毕')





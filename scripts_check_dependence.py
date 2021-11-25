# 作者仓库:https://github.com/spiritLHL/qinglong_auto_tools
# 觉得不错麻烦点个star谢谢


'''
cron: 1
new Env('二叉树修复脚本依赖文件');
'''


import os,requests
# from os import popen


# 只修复依赖文件（jdCookie.js那种）！！不修复环境依赖（pip install aiohttp）！！
# 默认不做任何操作只查询依赖脚本存在与否，有需求请在配置文件中配置对应变量进行操作，更新不会增加缺失文件
# 如果你有发现更多的脚本依赖文件没有新增，欢迎提交issues到https://github.com/spiritLHL/dependence_scripts/issues
# 增加缺失依赖文件
# export ec_fix_dep="true"
# 更新老旧依赖文件
# export ec_ref_dep="true"

try:
    if os.environ["ec_fix_dep"] == "true":
        print("已配置依赖文件缺失修复\n")
        fix = 1
    else:
        fix = 0
except:
    fix = 0
    print("默认不修复缺失依赖文件，有需求")
    print("请在配置文件中配置 export ec_fix_dep=\"true\" 开启脚本依赖文件缺失修复\n")

try:
    if os.environ["ec_ref_dep"] == "true":
        print("已配置依赖文件老旧更新\n")
        ref = 1
    else:
        ref = 0
except:
    ref = 0
    print("默认不更新老旧依赖文件，有需求")
    print("请在配置文件中配置 export ec_re_dep=\"true\" 开启脚本依赖文件更新\n")

res = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents").json()
dependence_scripts_name = []
for i in res:
    dependence_scripts_name.append(i["name"])


dir_list = os.listdir("./")

# 查询
for i in dependence_scripts_name:
    if i not in dir_list and i != "utils":
        print("缺失文件 {}".format(i))
        # 修补
        try:
            if fix == 1:
                print("增加文件 {}".format(i))
                r = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/spiritLHL/dependence_scripts/master/"+i).text
                with open(i, "w", encoding="utf-8") as fe:
                    fe.write(r)
        except:
            temp = 1

try:
    if temp == 1:
        print("未配置ec_fix_dep，默认不修复增加缺失的依赖文件")
except:
    pass

# 更新
try:
    if ref == 1:
        for i in dependence_scripts_name:
            if i != "utils":
                with open(i, "r", encoding="utf-8") as f:
                    r = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/spiritLHL/dependence_scripts/master/"+i).text
                    d = f.read()
                    if r == d:
                        print("无需修改 {}".format(i))
                    else:
                        print("更新文件 {}".format(i))
                        with open(i, "w", encoding="utf-8") as fe:
                            fe.write(r)
except:
    print("未配置ec_ref_dep，默认不更新依赖文件")



# utils

res = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/utils").json()
dependence_scripts_utils = []
for i in res:
    dependence_scripts_utils.append(i["name"])

try:
    utils_list = os.listdir("./utils")
except:
    os.makedirs("utils")

# 查询
for i in dependence_scripts_utils:
    if i not in utils_list and i != "utils":
        print("缺失文件 {}".format(i))
        # 修补
        try:
            if fix == 1:
                print("增加文件 {}".format(i))
                r = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/spiritLHL/dependence_scripts/master/"+i).text
                with open("./utils/"+i, "w", encoding="utf-8") as fe:
                    fe.write(r)
        except:
            temp = 1

try:
    if temp == 1:
        print("未配置ec_fix_dep，默认不修复增加缺失的依赖文件")
except:
    pass

# 更新
try:
    if ref == 1:
        for i in dependence_scripts_utils:
            if i != "utils":
                with open("./utils/"+i, "r", encoding="utf-8") as f:
                    r = requests.get("https://ghproxy.com/https://raw.githubusercontent.com/spiritLHL/dependence_scripts/master/utils/"+j).text
                    d = f.read()
                    if r == d:
                        print("已存在文件 {}".format(j))
                    else:
                        print("缺失文件 {}".format(j))
                        with open("./utils/txtx"+i, "w", encoding="utf-8") as fe:
                            fe.write(r)
except:
    print("未配置ec_ref_dep，默认不更新依赖文件")

# 待开发
# 修复依赖环境
# export ec_add_dep="true"
# docker exec -it qinglong bash -c "$(curl -fsSL https://ghproxy.com/https://raw.githubusercontent.com/FlechazoPh/QLDependency/main/Shell/QLOneKeyDependency.sh | sh)"
# try:
#     if os.environ["ec_add_dep"] == "true":
#         pass
# except:
#     pass
# text = os.popen("$(curl -fsSL https://ghproxy.com/https://raw.githubusercontent.com/FlechazoPh/QLDependency/main/Shell/QLOneKeyDependency.sh | sh)").read()
# print(text)
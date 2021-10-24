# qinglong_auto_tools


目录结构：

| 文件名字 | 用途 |
|  ----  | ----  |
| 2288 | 2.2和2.8青龙批量上传ck脚本 |
| Script | 个人修改的一些py脚本，自用，勿喷 |
| qq | qq相关脚本 |
| tg | tg相关脚本 |
| trs_stream.py | 本地转换stream抓到的headers为json格式，使用方法详见注释 |
| ck_auto_select.py | ck本地去重小工具，用法看注释 |  
| cks_push_alql.py | 多容器ck分发工具，方便多容器管理，用法详见注释 |
| cks_merge_alql.py | 多容器ck合并工具，方便多容器管理，用法详见注释 |
| cks_sync_able.py | 多容器同步环境变量启用禁用脚本，方便多容器管理，使用方法详见注释 |
| tasks_sync_able.py | 多容器同步任务启用禁用脚本，方便多容器管理，使用方法详见注释 |
| tasks_sync_scripts_able.py | 多容器同步已启用的脚本文件，方便多容器脚本更新管理，使用方法详见注释 |
| tasks_sync_all.py | 多容器无脑同步所有脚本文件和任务，方便多容器脚本迁移管理，使用方法详见注释 |

### 分容器相关脚本 

仅支持云服务器部署的2.9.0以上的青龙

| 文件名字 | 用途 |
|  ----  | ----  |
| cks_push_alql.py | 多容器ck分发工具，方便多容器管理，用法详见注释 |
| cks_merge_alql.py | 多容器ck合并工具，方便多容器管理，用法详见注释 |
| cks_sync_able.py | 多容器同步环境变量启用禁用脚本，方便多容器管理，使用方法详见注释 |
| tasks_sync_able.py | 多容器同步任务启用禁用脚本，方便多容器管理，使用方法详见注释 |
| tasks_sync_scripts_able.py | 多容器同步已启用的脚本文件，方便多容器脚本更新管理，使用方法详见注释 |
| tasks_sync_all.py | 多容器无脑同步所有脚本文件和任务，方便多容器脚本迁移管理，使用方法详见注释 |

青龙拉取命令：

```bash
ql repo https://ghproxy.com/https://github.com/spiritLHL/qinglong_auto_tools.git "tasks_|cks_"
```

### 适配火狐浏览器的青龙面板自动上传ck脚本

2288文件夹内文件需在同一文件夹里才可正常使用

| 文件名字 | 用途 |
|  ----  | ----  |
| push28.py | 适配2.8版本的脚本 |  
| push22.py | 适配2.2版本的脚本 |  
| ck.txt | 一行一个ck的文件 |   
| geckodriver.exe | 适配90.0.2 (64 位)火狐浏览器的driver |   

ps:批量上传ck的脚本不适配2.9！

下载环境:

cmd输入

```bash
pip install selenium
```

修改push28.py或push22.py的内容，填写用户名，密码，登陆地址(注意最后是以‘/’结束的)

ck形式，push28.py或push22.py默认使用形式一，有需要的自己注释掉形式一使用形式二

形式一：

ck.txt里放入ck，一行一个

形式二：

ck1&ck2&ck3

在编辑器运行run一下就自动化操作了，当然也可以```python xxx.py```在命令行操作运行

ps:网速不好的加载不出来页面请自行调高操作间隔，我设置的都是0.几秒

2021.10.24

更新仓库结构，更新机器人查询，更新自修改脚本

转载起码保留作者名谢谢


# 免责声明

* 代码仅供学习
* 不可用于商业以及非法目的,使用本代码产生的一切后果, 作者不承担任何责任.

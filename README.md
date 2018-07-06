# ERU-Manager version 1.0(Beta) CMDB 管理系统

## 系统介绍

ERU-Manager 是一个基于 Django 框架开发的一款 CMDB 管理系统, 目前处于 beta 版本, 功能主要包含: 管理系统管理的客户主机列表, 
动态显示客户机状态信息, 远程指令操作指定客户机, 主机与客户机之间的文件传输以及完善的后台管理系统。

## 功能描述:

1. 云主机的信息统计
2. 数据的动态展示
3. 远程指令控制
4. 文件传输
5. 完善的后台管理系统

## 开发环境

- win10
- Python3.6
- paramiko2.4.1
- xadmin0.6.1
- sqlite3

## 整体架构

![](https://i.imgur.com/9O5LavC.png)

## 使用说明及展示

> 注: 本次使用说明基于本地IP端口, 直接访问 http://127.0.0.1:8000 即可

## 开启系统

第一种方法:

- 命令行切换到项目的根目录下 `/eru_manager` 下, 执行命令 `python manage.py runserver 0.0.0.0:8000`, 这里让系统启动并设置 IP 为 `0.0.0.0` 目的是可以让客户端访问。

第二种方法:

- 直接把本项目导入到 `PyCharm` 中运行即可

## 管理员注册

新人访问系统, 首先需要注册一个账号, 注册地址 `http://127.0.0.1:8000/manager/register`

![](https://i.imgur.com/bhjtGfh.png)

## 登录

注册成功以后, 会自动跳转到登录页面, 用刚才注册的账号登录即可。

若不想登录, 直接用此账号登录即可：

- admiin
- 123456

![](https://i.imgur.com/bJXqR1S.png)

进入首页, 可以看到本系统的基本介绍和功能选择界面

![](https://i.imgur.com/8lYHTFa.png)

自登录进来以后, 会自动保存管理员信息在本地 cookie 中, 有效期为 1小时, 也就是说1小时以后, 系统要求管理员重新登录, 否则自动退出

下面一次介绍每个功能

## 主机列表

在这个页面中, 展示了目前已经在管理的客户主机信息, 其中包含 `主机的IP`, `自定义名称`, `操作系统`, `CPU型号`, 以及 `最近的一次重启时间`.

![](https://i.imgur.com/KzPU1fm.png)

在这个页面, 管理员可以直接操作删除目前管理的客户主机, 将不再对其监控。 也可以添加一个新的主机进来, 点击`新增`按钮, 跳转至添加页面, 将要添加的主机IP, 可以把管理员信息填进去, 系统会自动去读取管理的主机相关信息, 并保存到数据库, 添加成功

![](https://i.imgur.com/aAw0eKn.png)

## 动态信息

这个页面作为一个信息动态的展示, 因为要想显示更多的信息, 只是在脚本中, 去多读取一些信息, 发送回来, 分图表去展示, 这里目前只收集一个客户机发送上来的 CPU 信息用来做例子展示。

![](https://i.imgur.com/Rn0sU2e.png)

> 这个页面想要看到数据的动态变化, 需要将本项目中的 `send_data.py` 文件运行, 配置好服务器的IP(比如我win10的ip地址是`192.168.76.42`), 并使用一会要说到的第四个文件分发的功能将这个文件, 下发到客户机上去运行起来。 这样就能看到这个页面对应客户主机的动态信息啦。

## 远程指令

在这个页面有两个功能:

1. 给指定远程主机发出指令, 并执行获取结果
2. 查看最近执行成功的 7 条指令

#### 发送指令

下面的例子中, 我向我的阿里云主机发送了一条 `ls /home/zhaopf/erublog`, 查看我的用户目录下的`erublog` 项目下的文件信息, 右边的黑色框中会显示收到的信息。 若链接主机失败, 会在右侧的显示框, 提示链接不成功。

![](https://i.imgur.com/lllDtY7.png)

#### 发送指令历史

点击 `发送历史` 按钮, 会在右侧框中显示历史记录, 格式为 `发送时间>>发送指令>>远程主机ip`

![](https://i.imgur.com/PRmOeBY.png)

## 文件传输

这个页面同样也有两个功能:

1. 向服务器上传文件
2. 向指定的 IP 远程主机, 分发文件

成功则在页面提示发送成功, 失败则提示发送失败

具体使用请参考下面图片:

#### 上传文件

上传成功以后, 会保存在项目根目录下的 `upload` 中。

![](https://i.imgur.com/GPlZs9V.png)

#### 分发文件

![](https://i.imgur.com/SW3gAR4.png)

我们到 `172.31.236.106`这个IP的主机中去看一下, 文件是否发送成功?

![](https://i.imgur.com/K9yC61O.png)

从上图可以看出, 主机IP `172.31.236.106` 成功接收到了我们刚从 win10 发送的 `requirements.txt` 文件

#### 后台管理系统

> xadmin是django的第三方扩展, 可使django的admin站点使用更方便

#### 安装

通过如下命令安装 `xadmin` 的最新版:

	pip install https://github.com/sshwsfc/xadmin/tarball/master

在配置文件中注册如下应用:

	INSTALLED_APPS = [
	    ...
	    'xadmin',
	    'crispy_forms',
	    'reversion',
	    ...
	]

`xadmin` 有建立自己的数据库模型类, 需要进行数据库迁移:

	python manage.py makemigrations
	python manage.py migrate

在总路由中添加`xadmin`的路由信息

	import xadmin
	
	urlpatterns = [
	    # url(r'^admin/', admin.site.urls),
	    url(r'xadmin/', include(xadmin.site.urls)),
	    ...
	]

#### 使用

- `xadmin`不再使用 django的admin.py, 而是需要编写代码在`adminx.py` 文件中。
- `xadmin`的站点管理类不再继承`admin.ModelAdmin`, 而是直接继承 `object` 即可

在 `manager` 应用下创建`adminx.py` 文件

下面我只简单的说下关于`xadmin`的一些配置, 具体可以参考github上的链接: [https://github.com/sshwsfc/xadmin](https://github.com/sshwsfc/xadmin)

	class BaseSetting(object):
	    """xadmin基本配置"""
	    enable_themes = True # 开启主题切换功能
	    use_bootswatch = True
	
	
	xadmin.site.register(views.BaseAdminView, BaseSetting)
	
	
	class GlobalSettings(object):
	    """xadmin的全局配置"""
	    site_title = 'Eru-Manager'  # 设置站点标题
	    site_footer = 'Eru-Manager' # 设置站点的页脚
	    menu_style = 'accordion' # 设置菜单折叠
	
	
	xadmin.site.register(views.CommAdminView, GlobalSettings)
	
	
	class HostAdmin(object):
	    model_icon = 'fa fa-list'  # 显示图标
	    list_display = ['id', 'host_name', 'os', 'cpu', 'last_login_time', 'is_delete']  # 需要显示的主机信息
	    search_fields = ['id', 'host_name']  # 搜索需要用到的字段
	    list_editable = ['host_name', 'is_delete'] # 可编辑的主机字典
	    show_bookmarks = True  # 是否启用书签
	    list_export = ['xls', 'csv', 'xml']  # 能导出的类型xls, csv, xml

	xadmin.site.register(models.HostInfo, HostAdmin)

![](https://i.imgur.com/LRDd2hB.png)


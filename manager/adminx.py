import xadmin
from xadmin import views

from . import models
from showdata.models import CPUData
from remoteCMD.models import CmdList


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
    model_icon = 'fa fa-list'
    list_display = ['id', 'host_name', 'os', 'cpu', 'last_login_time', 'is_delete']
    search_fields = ['id', 'host_name']
    list_editable = ['host_name', 'is_delete']
    show_bookmarks = True
    list_export = ['xls', 'csv', 'xml']


xadmin.site.register(models.HostInfo, HostAdmin)


class UserAdmin(object):
    model_icon = 'fa fa-user'
    list_display = ['id', 'name', 'password', 'email']


xadmin.site.register(models.UseInfo, UserAdmin)


class CMDAdmin(object):
    model_icon = 'fa fa-keyboard-o'
    list_display = ['id', 'cmd', 'host', 'time']


xadmin.site.register(CmdList, CMDAdmin)


class CPUAdmin(object):
    model_icon = 'fa fa-sitemap'
    list_display = ['id', 'data', 'time']


xadmin.site.register(CPUData, CPUAdmin)
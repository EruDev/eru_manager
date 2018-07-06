from django.conf.urls import url
from . import views
from remoteCMD.views import remote_cmd, file_trans
from showdata.views import show_data, save_data, get_data

urlpatterns = [
    url(r'^login/$',views.login, name='login'),
    url(r'^register/$',views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^hostlist/$', views.hostlist, name='hostList'),
    url(r'^add_host/$', views.add_host, name='add_host'),
    url(r'^del_host/$', views.del_host, name='del_host'),
    url(r'^remote_cmd/$', remote_cmd, name='remote_cmd'),
    url(r'^file_trans/$', file_trans, name='file_trans'),
    url(r'^show_data/$', show_data, name='show_data'),
    url(r'^save_data/$', save_data, name='save_data'),
    url(r'^get_data/$', get_data, name='get_data'),
]
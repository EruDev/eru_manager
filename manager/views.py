import hashlib
from django.shortcuts import render, reverse, redirect
from .models import UseInfo, HostInfo
from remoteCMD.remote import Remote

# Create your views here.
def hash_password(password):
    """
    md5加密
    :param password:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def is_user_exist(username):
    """
    检查用户名是否存在
    :param username:
    :return:
    """
    if UseInfo.objects.filter(name=username):
        return True
    return False


def login_check(func):
    """
    用户登录验证
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        name = request.COOKIES.get('name')
        if not name:
            return redirect(reverse('login'))
        return func(request, *args, **kwargs)
    return wrapper


def login(request):
    if request.method == 'POST' and request.POST:
        username = request.POST['name']
        password = request.POST['password']
        password = hash_password(password)
        print(password)
        # email = request.POST['email']

        if is_user_exist(username):
            db_passwd = UseInfo.objects.get(name=username).password
            print(db_passwd)
            if password == db_passwd:
                response = redirect(reverse('index'))
                response.set_cookie('name', username, max_age=3600)
                request.session['name'] = username

                return response
            else:
                error = '用户名或者密码错误, 请重新输入'
                return render(request, 'login.html', locals())
        else:
            error = '用户名或者密码错误, 请重新输入'
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html', locals())


def logout(request):
    """
    退出
    :param request:
    :return:
    """
    request.session.clear()
    response = redirect(reverse('login'))
    response.delete_cookie('name')
    return response

def register(request):
    if request.method == 'POST' and request.POST:
        username = request.POST['name']
        if is_user_exist(username):
            warn = '用户名已经存在, 请重新输入'
            return render(request, 'register.html', locals())
        else:
            user = UseInfo()
            user.name = username
            password = request.POST['password']
            email = request.POST['email']
            user.password = hash_password(password)
            user.email = email
            user.save()
            return redirect(reverse('login'))
    else:
        return render(request, 'register.html')


@login_check
def index(request):
    """首页"""
    username = request.COOKIES.get('name', '')
    return render(request, 'index.html', locals())


@login_check
def hostlist(request):
    username = request.COOKIES.get('name', '')
    host_list = HostInfo.objects.filter(is_delete=False)
    return render(request, 'hostlist.html', locals())


def get_host_info(ip, admin, password, nickname):
    """获取主机信息"""
    try:
        r = Remote(host=ip, username=admin, password=password)
        db_host = HostInfo()
        db_host.ip = ip
        db_host.host_name = nickname
        db_host.cpu = str(r.ssh('cat /proc/cpuinfo | grep name |cut -f2 -d:')[0].replace('\n', '')) # cpu信息
        db_host.os = str(r.ssh('cat /etc/issue')[0].replace('\\n', '').replace('\\l\n', '')) # 系统版本
        db_host.last_login_time = str(r.ssh("who -b | cut -d ' ' -f 13,14")[0].replace('\n', '')) # 上次登录时间
        db_host.is_delete = False
        db_host.save()
        return True
    except Exception as e:
        print(e)
        return False



@login_check
def add_host(request):
    """添加主机"""
    username = request.COOKIES.get('name', '')
    if request.method == 'POST' and request.POST:
        host_ip = request.POST['ip']
        nickname = request.POST['nickname']
        password = request.POST['password']
        admin = request.POST['admin']
        if get_host_info(host_ip, admin, password, nickname):
            is_add = 0
            return render(request, 'add_host.html', locals())
        else:
            is_add = 1
            return render(request, 'add_host.html', locals())
    return render(request, 'add_host.html', locals())


@login_check
def del_host(request):
    """删除主机"""
    del_id = request.GET.get('id', '')
    host = HostInfo.objects.get(id=del_id)
    host.is_delete = True
    host.save()
    return redirect(reverse('hostList'))
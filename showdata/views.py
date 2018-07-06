from django.shortcuts import render
from django.http import JsonResponse
from manager.views import login_check
from .models import CPUData


# 接收客户端主机发送过来的数据 POST
def save_data(request):
    result = {'status': 'error', 'err_msg': ''}
    if request.method == 'POST' and request.POST:
        data = request.POST['data']
        time = request.POST['time']

        cpu = CPUData()
        cpu.data = data
        cpu.time = time
        cpu.save()
        result['status'] = 'success'
        result['err_msg'] = 0
    else:
        result['err_msg'] = '请求方法必须为 POST, 不能为空'
    return JsonResponse(result)


# 读取数据库中最新的一条数据
def get_data(request):
    data = CPUData.objects.order_by('-id')[0]
    time = data.time
    result = {
        'time': time.strftime('%H:%M:%S'),
        'data': data.data
    }
    return JsonResponse(result)


@login_check
def show_data(request):
    username = request.COOKIES.get('name', '')
    return render(request, 'show_data.html', locals())


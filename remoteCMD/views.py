from datetime import datetime

import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from manager.views import login_check
from .models import CmdList
from .remote import Remote, Sftp


showFlag = ''
@login_check
def remote_cmd(request):
    username = request.COOKIES.get('name', '')
    if request.method == 'POST' and request.POST:
        # 发送指令
        if 'sendcmd' in request.POST:
            ip = request.POST['ip']
            user = request.POST['username']
            password = request.POST['password']
            cmd = request.POST['cmd']
            # print(ip, user, password, cmd)
            if request.POST['port']:
                port = int(request.POST['port']) # 这里要转成整型!!!!
            else:
                port = 22
            # 存储到历史命令
            db_cmd = CmdList()
            db_cmd.host = ip
            db_cmd.cmd = cmd
            time = datetime.now()
            db_cmd.time = time
            db_cmd.save()
            # 远程发送指令
            handler = Remote(host=ip, username=user, password=password, port=port)
            remote = handler.ssh(cmd)
            # print(remote)
            showFlag = 'remote'
            return render(request, 'remote_cmd.html', locals())
        elif 'history' in request.POST:
            # 查询最近 6 条命令
            cmds = CmdList.objects.order_by('-id')[:6]
            results = []
            for item in cmds:
                results.append({
                    'time': item.time.strftime('%m-%d %H:%M:%S'),
                    'cmd': item.cmd,
                    'host': item.host,
                })
            showFlag = 'result'
            return render(request, 'remote_cmd.html', locals())
        else:
            return render(request, 'remote_cmd.html')
    else:
        return render(request, 'remote_cmd.html')


@login_check
def file_trans(request):
    """文件传输"""
    username = request.COOKIES.get('name', '')
    if request.method == 'POST' and request.POST:
        if 'upload' in request.POST: # 文件上传
            if 'upload_file' in request.FILES:
                file = request.FILES.get('upload_file', '')
                save_path = default_storage.save('../eru_manager/upload/' + file.name, ContentFile(file.read()))
                tmp_file = os.path.join(settings.BASE_DIR, save_path)
                is_success = True
                upload_tips = '上传成功'
                return render(request, 'file_trans.html', locals())
            else:
                is_success = False
                upload_tips = '上传失败'
                return render(request, 'file_trans.html', locals())
        elif 'put_file' in request.POST: # 文件分发
            des_ip = request.POST['des_ip']
            client_user = request.POST['client_user']
            client_passwd = request.POST['client_passwd']
            put_file_path = request.POST['put_file_path']
            save_path = request.POST['save_path']

            sftp = Sftp(hostip=des_ip, username=client_user, passwd=client_passwd)

            try:
                if save_path:
                    sftp.put(put_file_path, save_path)
                else:
                    sftp.put(put_file_path)
                is_put = True
                put_tips = '发送成功'
                return render(request, 'file_trans.html', locals())
            except Exception as e:
                print(e)
                is_put = False
                put_tips = '发送失败'
                return render(request, 'file_trans.html', locals())
        else:
            return render(request, 'file_trans.html', locals())
    return render(request, 'file_trans.html', locals())


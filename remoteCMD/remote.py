import os
import paramiko


class Remote(object):

    def __init__(self, host, username, password, port=22):
        """初始化参数"""
        self.host = host
        self.usename = username
        self.password = password
        self.port = port

    def ssh(self, cmd):
        self.cmd = cmd
        try:
            # 基于paramiko.Transport 的连接方式
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.usename, password=self.password)
        except Exception as e:
            print(e)
            return False
        else:
            # 基于paramiko.SSHClient() 的连接方式
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh._transport = transport
            stdin, stdout, stderr = ssh.exec_command(self.cmd)
            result = stdout.readlines()
            transport.close()
            return result


class Sftp(object):

    def __init__(self, hostip, username, passwd, port=22):
        self.hostip = hostip
        self.username = username
        self.passwd = passwd
        self.port = port

    def ssh(self):
        try:
            self.transport = paramiko.Transport((self.hostip, self.port))
            self.transport.connect(username=self.username, password=self.passwd)
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def put(self, upload_file, remote_path='/home/tmp/'):
        """上传文件"""
        # 如果能够链接成功
        if self.ssh():
            self.upload_file = upload_file.replace('\\', '/')  # 上传文件的路径 类似于C:\Code\cat.jpg
            self.remote_path = remote_path + os.path.split(self.upload_file)[-1]  # 主机上的文件路径  类似于/tmp/cat.jpg
            print('本地上传路径', self.upload_file)
            print('远程服务器路径', self.remote_path)

            sftp = paramiko.SFTPClient.from_transport(self.transport)
            sftp.put(self.upload_file, self.remote_path)
            self.transport.close()
            print('上传成功')

    def get(self, getfile, savepath):
        self.getfile = getfile
        self.savepath = savepath

        # 如果能够链接成功
        if self.ssh():
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            # 将服务器上的路径getfile 下载到本地路径savepath
            sftp.get(self.getfile, self.savepath)
            self.transport.close()


# if __name__ == '__main__':
# #     # r = Remote(host='47.105.48.255', username='root', password='****', port=22)
# #     # result = r.ssh('cat /etc/issue')[0].replace('\\n', '').replace('\\l\n', '')
# #     # print(result)
#     sftp = Sftp(hostip='47.105.48.255', username='root', passwd='****')
#     upload_file = 'C:\\Code\\test.txt'
#     remote_path = '/home/zhaopf/'
#     sftp.put(upload_file, remote_path)
    # print(upload_file)
    # print(remote_path)
    # print('上传成功')







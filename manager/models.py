from django.db import models

# Create your models here.
# 用户表
class UseInfo(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    email = models.CharField(max_length=128, verbose_name='邮箱')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


# 主机表
class HostInfo(models.Model):
    ip = models.CharField(max_length=128, verbose_name='ip')
    host_name = models.CharField(max_length=128, verbose_name='主机名')
    os = models.CharField(max_length=128, verbose_name='操作系统')
    cpu = models.CharField(max_length=128, verbose_name='cpu型号')
    last_login_time = models.CharField(max_length=128, verbose_name='上次登录时间')
    is_delete = models.BooleanField(verbose_name='删除标志')

    def __str__(self):
        return self.host_name

    class Meta:
        verbose_name = '主机表'
        verbose_name_plural = verbose_name
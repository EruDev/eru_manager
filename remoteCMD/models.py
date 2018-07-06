from django.db import models

# Create your models here.
class CmdList(models.Model):
    cmd = models.CharField(max_length=128, verbose_name='命令')
    host = models.CharField(max_length=128, default='47.105.48.255', verbose_name='主机')
    time = models.DateTimeField(verbose_name='发出命令的时间')

    class Meta:
        verbose_name = '命令表'
        verbose_name_plural = verbose_name
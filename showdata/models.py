from django.db import models


class CPUData(models.Model):
    data = models.CharField(max_length=128, verbose_name='CPU数据')
    time = models.DateTimeField(verbose_name='监听时间')

    class Meta:
        verbose_name = 'CPU数据表'
        verbose_name_plural = verbose_name

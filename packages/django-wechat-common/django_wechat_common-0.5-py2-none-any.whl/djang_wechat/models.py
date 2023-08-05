# -*- coding:UTF-8 -*-
from django.db import models

# Create your models here.

class Wechat(models.Model):
    """当前微信token"""""
    token = models.CharField(u'token', max_length=255, blank=True, null=True)
    token_create_time = models.DateTimeField(u'token创建时间', max_length=255, blank=True, null=True)
    create_time=models.DateTimeField(u'创建时间',auto_now_add=True)
    def __unicode__(self):
        return self.token
    class Meta:
        verbose_name=u'当前微信token'
        verbose_name_plural=verbose_name



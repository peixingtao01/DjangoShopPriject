from __future__ import absolute_import,unicode_literals
# 上面这个必须在这一行
import os
from celery import Celery
from django.conf import settings
# 设置celery执行的环境变量，执行Django项目的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE','CeleryTask.settings')
# 创建celery应用
app = Celery('art_project')#应用名称
app.config_from_object('django.conf:settings')#Django的配置文件
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)



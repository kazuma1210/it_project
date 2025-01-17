"""
WSGI config for it_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_project.settings')

application = get_wsgi_application()

import os
import sys

# プロジェクトディレクトリを追加
path = '/home/nikakih/it_project'
if path not in sys.path:
    sys.path.append(path)

# Djangoの設定を指定
os.environ['DJANGO_SETTINGS_MODULE'] = 'it_project.settings'

# アプリケーションを起動
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

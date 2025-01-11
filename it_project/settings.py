import pymysql
from pathlib import Path
import os

# MySQLdb を使用するための設定
pymysql.install_as_MySQLdb()

# プロジェクトの基本ディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# セキュリティ警告: 本番環境ではSECRET_KEYを隠して管理する
SECRET_KEY = 'django-insecure-_ebj55x)g$g0051_z%%%k!9!dk$q38xv8fy6!9iw$)@v6l3(rg'

DEBUG = True
ALLOWED_HOSTS = []

# アプリケーション設定
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # ここにアプリケーション名を追加
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

]

ROOT_URLCONF = 'it_project.urls'

# テンプレート設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/1_user'),  # 1_user内の全テンプレートを扱う
            os.path.join(BASE_DIR, 'templates/2_admin'), # 2_admin内の全テンプレートを扱う
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'it_project.wsgi.application'

# データベース設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hakatakoyu',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}

# パスワード検証設定
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]  # リストを閉じ忘れを修正

# 言語とタイムゾーンの設定
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# 静的ファイルのURL設定
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# デフォルトのプライマリキー設定
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# メール送信の設定
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_HOST_USER = '15ad0f22a9098e'
EMAIL_HOST_PASSWORD = '74eded4009c27c'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'your_email@example.com'

AUTH_USER_MODEL = 'app.CustomUser'
AUTH_USER_MODEL = 'auth.User'

DEFAULT_INDEX_LENGTH = 191
"""
CI/CD 測試環境設定
"""
from .settings import *
import os

# 測試環境設定
DEBUG = True
SECRET_KEY = 'test-secret-key-for-ci-testing-only'

# 資料庫設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'woodsdb_test',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 安全設定
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# 關閉一些在測試時不需要的功能
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# 靜態文件設定
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 媒體文件設定
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')

# 簡化的CORS設定
CORS_ALLOW_ALL_ORIGINS = True

# 測試時關閉緩存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
} 
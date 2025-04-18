"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / '.config_secret' / 'secret.json') as f:
    config_secret_str = f.read()

SECRET = json.loads(config_secret_str)  # json 형태를 딕셔너리 형태로 바꿈


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY가 노출되면 보안상 위험하기 때문에 secret.json을 사용
# SECRET_KEY = 'django-insecure-q#!@4g=92+#a(qre&!&+(4&z8m7@60_eq09rna_jdby)&41pte'
SECRET_KEY = SECRET['DJANGO_SECRET_KEY']
# print(f'secret key {SECRET["DJANGO_SECRET_KEY"]}')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# DEBUG = False
# ALLOWED_HOSTS = [
#     '127.0.0.1',
#     'localhost',
# ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # own
    'member',
    'post',
    # 3rd party
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# 개발 환경에서 사용하는 경로
STATIC_URL = 'static/'
STATIC_DIR = BASE_DIR / 'static'

STATICFILES_DIRS = [
    STATIC_DIR,
]

# 배포할 때 사용하는 경로
STATIC_ROOT = BASE_DIR / '.static_root'

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth
AUTH_USER_MODEL = 'member.User'  # 유저 모델 지정

# 이런식으로 아이디랑 비밀번호 설정해놓고 같이 깃에 올라가면 누군가 볼 수도있고
# 비공개 리파짓토리라도 중간에 탈취당할 위험이 있음.
# 그래서 환경변수를 사용해서 정보를 내 컴퓨터에서 읽어오도록함.
# EMAIL_HOST_USER = 'test@gmail.com'
# EMAIL_HOST_PASSWORD = '1111'

# Email
# from django.core.mail.backends.smtp import EmailBackend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.naver.com' # 네이버 환결설정에서 볼 수 있음.
EMAIL_USE_TLS = True  # 보안연결
EMAIL_PORT = 587  # 네이버 메일 환경설정에서 확인 가능
EMAIL_HOST_USER = SECRET["email"]["user"]
EMAIL_HOST_PASSWORD =  SECRET["email"]["password"]

# .config_secret 폴더 만들고
# 폴더에 secret.json 만들고
# .gitignore에 추가한 후 관리
# print(SECRET['DB']['HOST'])
# print(SECRET['DB2']['HOST'])
# 이렇게 쓸 수도있고 dotenv를 통해 관리할 수도 있음

LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'
# LOGOUT_REDIRECT_URL = '/'

# OAuth
NAVER_CLIENT_ID = SECRET["naver"]["client_id"]
NAVER_CLIENT_SECRET = SECRET["naver"]["secret"]

GITHUB_CLIENT_ID = SECRET["github"]["client_id"]
GITHUB_CLIENT_SECRET = SECRET["github"]["secret"]
from django.urls import path
from . import oauth_views

app_name = 'oauth'
urlpatterns = [
    path('naver/login/', oauth_views.NaverLoginRedirectView.as_view(), name='naver_login'),

]
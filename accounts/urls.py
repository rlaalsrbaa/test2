from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signin/kakao/', views.kakao_signin, name='kakao_signin'),
    path('signin/kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('signout/', views.signout, name='signout'),
]

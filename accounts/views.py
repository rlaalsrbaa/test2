import os

import requests

from django.contrib import messages
from django.contrib.auth.views import logout_then_login, LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, login
from accounts.forms import SignupForm

def signout(request: HttpRequest):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request,'accounts:signin')


signin = LoginView.as_view(template_name='accounts/signin.html')


def signup(request: HttpRequest):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입 환영합니다.")
            # signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천.
            next_url = request.GET.get('next', '/')
            return redirect('products:list')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })

def kakao_signin(request: HttpRequest):
    REST_API_KEY = os.environ.get("KAKAO_APP__REST_API_KEY")
    REDIRECT_URI = os.environ.get("KAKAO_APP__LOGIN__REDIRECT_URI")

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code"
    )


class KakaoException:
    pass


def kakao_callback(request):

    #(1)
    code = request.GET.get("code")
    REST_API_KEY = os.environ.get("KAKAO_APP__REST_API_KEY")
    REDIRECT_URI = os.environ.get("KAKAO_APP__LOGIN__REDIRECT_URI")

    #(2)
    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
    )
    #(3)
    token_json = token_request.json()
    error = token_json.get("error", None)
    if error is not None:
        raise KakaoException()

    # (4)
    access_token = token_json.get("access_token")

    # (5)
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    id = profile_json.get("id")

    user = authenticate(request, username="kakao__" + str(id), password="")
    if user is not None:
        login(request, user=user)
        messages.success(request, "로그인 되었습니다.")
        return redirect('/')

    return HttpResponse(user)
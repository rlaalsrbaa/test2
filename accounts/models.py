from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from django.db.models import QuerySet


class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = "male", "남성"
        FEMALE = "female", "여성"

    gender = models.CharField('성별', max_length=6, blank=True, choices=GenderChoices.choices)
    avatar = models.ImageField('아바타', blank=True, upload_to="accounts/avatar/%Y/%m/%d",
                               help_text="100px * 100px 크기의 gif/png/jpg 이미지를 업로드해주세요.")
    class ProviderTypeCodeChoices(models.TextChoices):
        LOCAL = "local", "로컬"
        KAKAO = "kakao", "카카오"

    provider_type_code = models.CharField('프로바이더 타입 코드', max_length=20, choices=ProviderTypeCodeChoices.choices,
                                          default=ProviderTypeCodeChoices.LOCAL)
    provider_accounts_id = models.PositiveIntegerField('프로바이더 회원번호', default=0)
    @staticmethod
    def signin_with_kakao(provider_accounts_id):
        provider_type_code = User.ProviderTypeCodeChoices.KAKAO
        qs: QuerySet = User.objects.filter(provider_type_code=provider_type_code,
                                          provider_accounts_id=provider_accounts_id)
        if not qs.exists():
            username = provider_type_code + "__" + str(provider_accounts_id)
            name = provider_type_code + "__" + str(provider_accounts_id)
            email = ""
            password = ""
            User.objects.create_user(username=username, email=email,password=password, first_name=name,
                                     provider_type_code=provider_type_code, provider_accounts_id=provider_accounts_id)


    # authenticate(user=user)
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField('이름', max_length=50, null = True)
    email = models.EmailField('이메일', unique=True)
    password = models.CharField('비밀번호', max_length=128)
    user_type = models.CharField('유저타입', max_length= 10, default='') # {내담자 : 0, 상담사 : 1}

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    objects = CustomUserManager()

    realname = models.CharField('이름', blank=True, max_length=50)
    phone = models.CharField('휴대폰번호', blank=True, max_length=100)
    address = models.CharField('주소', blank=True, max_length=200)
    date_of_birth = models.DateField('생년월일', blank=True, null=True)

    def __str__(self):
        return self.email

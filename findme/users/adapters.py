from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import validate_email
from .token import account_activation_token
from .text import message
from users.models import User

class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_field
       # data = form.cleaned_data
       # user.username = data.get('username')
       # user.email = data.get('email')
       # user.user_type = data.get('user_type')
       # if 'password1' in data:
       #     user.set_password(data['password1'])
       # else:
       #     user.set_unusable_password()

        user = super().save_user(request, user, form, False)
        user_field(user, 'user_type', request.data.get('user_type'))
        user_field(user, 'introduce', request.data.get('introduce'))
        user_field(user, 'career', request.data.get('career'))
        user.save()
        currnet_site =get_current_site(request)
        domain = "http://ec2-13-209-32-113.ap-northeast-2.compute.amazonaws.com/"
        uidb64 = urlsafe_base64_encode(force_bytes(user.email))
        token = account_activation_token.make_token(user)
        message_data= message(domain,uidb64,token)
        mail_title = "FIND ME 인증 메일 입니다."
        mail_to = user.email 
        email = EmailMessage(mail_title,message_data,to=[mail_to])
        email.send()

        return user

from allauth.account.adapter import DefaultAccountAdapter


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
        user.save()
        return user

from django.test import TestCase, Client
from .models import User
# Create your tests here.
class UserTest(TestCase):
    # test용 데이터
    def setUp(self):
        self.client = Client()
        self.user= User()
    
        user=User.objects.create(email="rlaa@gmail.com")
        user.set_password('abcd123!!!')
        user.save()
    # 이메일 중복 test
    def test_redundant_check(self):
        response = self.client.get('/users/email',data={'email':'rlaa@gmail.com'})
        self.assertEqual(response.status_code, 403) 

    # 회원가입 test
    def test_user_registration(self):

        regi_info ={
            "username": "",
            "email":"@gmail.com",
            "user_type":"1",
            "password1":"!@#",
            "password2":"!@#" 
        }
        response= self.client.post('/rest-auth/registration/',data=regi_info)
        self.assertEqual(response.status_code,201)
        self.assertEqual(len(response.json().get("key"))>10,True)
    #로그인 test
    def test_user_login(self):
        #smoke test
        login_info={
            'email' : '',
            'password' : 'abcd123!!!',
            'user_type': 1
        }
        #로그인이 안됨
        response = self.client.post('/rest-auth/login/',data=login_info)
        print(response.json())
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json().get("key"))>10,True)
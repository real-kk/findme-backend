from django.test import TestCase, Client
from .models import User
from rest_framework.authtoken.models import Token
from django.core.files.images import ImageFile
import tempfile

# Create your tests here.
class UserTest(TestCase):
    # test용 데이터
    def setUp(self):
        self.client = Client()
    
        self.user=User.objects.create(email="rlaa@gmail.com")
        self.user.set_password('abcd123!!!')
        self.user.save()
        self.user_id = self.user.id
        token, created = Token.objects.get_or_create(user=self.user)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    # 이메일 중복 test
    def test_redundant_check(self):
        response = self.client.get('/users/email',data={'email':'rlaa@gmail.com'})
        self.assertEqual(response.status_code, 403) 

    # 회원가입 test
    def test_user_registration(self):
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image_mock= ImageFile(file, name=file.name)
        regi_info ={
            "username": "testname",
            "email":"test@gmail.com",
            "user_type":"1",
            "password1":"abcd123!!!",
            "password2":"abcd123!!!",
            "image":image_mock 
        }
        response= self.client.post('/rest-auth/registration/',data=regi_info)
        self.assertEqual(response.status_code,201)
        self.assertEqual(len(response.json().get("key"))>10,True)
    #로그인 test
    def test_user_login(self):
        #smoke test
        login_info={
            'email' : 'rlaa@gmail.com',
            'password' : 'abcd123!!!',
            'user_type': 1
        }
        response = self.client.post('/rest-auth/login/',data=login_info)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json().get("key"))>10,True)

    #약력 수정 test  lambda 에 있는 이미지를 사용해야하기때문에 오류가 뜬다.
    def test_user_update(self):
        #smoke test
        info={
            'introduce':'약력 대학교1년 대학교2년 대학교3년'
        }
        #로그인이 안됨
        response = self.client.put('/users/'+str(self.user_id)+"/",data=info,content_type='application/json')
        # self.assertEqual(response.status_code,200)
        # self.assertEqual(response.json(),'User was Updated')
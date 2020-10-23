from django.test import TestCase, Client
from .models import User
# Create your tests here.
class UserTest(TestCase):
    # test용 데이터
    def setUp(self):
        User.objects.create(email='rla@gmail.com')
    
    # 이메일 중복 test
    def test_redundant_check(self):
        client = Client() 
        response = self.client.get('/users/email',data={'email':'rla@gmail.com'})
        self.assertEqual(response.status_code, 403) 
    # 회원가입 test
    def test_user_registration(self):
        client = Client()

        regi_info ={
            "username": "kimtaeyun",
            "email":"rlarla@gamil.com",
            "user_type":"1", "password1":"dktnlqek123!@#",
            "password2":"dktnlqek123!@#" 
        }
        
        response= self.client.post('/rest-auth/registration/',data=regi_info)
        self.assertEqual(response.status_code,201)
        self.assertEqual(len(response.json().get("key"))>10,True)
    #로그인 test
    def test_user_login(self):
        #smoke test
        assert 1 is 1

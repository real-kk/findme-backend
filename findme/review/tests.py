import sys
sys.path.append("..")

from django.test import TestCase,Client
from .models import Review
from users.models import User
from rest_framework.authtoken.models import Token
# test용 데이터
class ReviewTest(TestCase):

    def setUp(self):
        self.review = Review()
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',                                                    
        )                                                                             
        token, created = Token.objects.get_or_create(user=self.user)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    # 회원가입 test
    def test_review_upload(self):
        
        review_info ={
            "counselor": "super@gmail.com",
            "content":"test review content",
        }
        response= self.client.post('/reviews/',data=review_info)
        self.assertEqual(response.status_code,201)


    def tearDown(self):
        # Clean up after each test
        self.user.delete()
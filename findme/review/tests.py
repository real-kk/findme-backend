import sys
sys.path.append("..")
import json 

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
            username='강낭콩'                                                    
        )
        client1 = User.objects.only('id').get(email='super@gmail.com')
        self.review=Review.objects.create(
            client=client1,
            counselor=client1,
            content="너무좋았어요"
        )
        token, created = Token.objects.get_or_create(user=self.user)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    # 리뷰 업로드 test
    def test_review_upload(self):
        
        review_info ={
            "counselor":"super@gmail.com",
            "content":"test review content",
        }
        response= self.client.post('/reviews/',data=review_info)
        self.assertEqual(response.status_code,201)
    # 리뷰 수정 test
    def test_review_update(self):
        review_info={
            "review_id":1,
            "content" :" 수정됨 " 
        }
        response= self.client.put('/reviews/',data=json.dumps(review_info),content_type='application/json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data ,'Review updated success')
    def tearDown(self):
        # Clean up after each test
        self.user.delete()
        self.review.delete()
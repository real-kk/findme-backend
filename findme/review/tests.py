import sys
sys.path.append("..")
import json 
from django.db.models.fields.related import ForeignKey
from django.test import TestCase,Client
from .models import Review
from users.models import User
from rest_framework.authtoken.models import Token
class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )
        Review.objects.create(
            client=self.user,
            counselor=self.user,
            content="너무좋았어요"
        )
        Review.objects.create(
            client=self.user,
            counselor=self.user,
            content="너무좋았어요"
            
        )
        self.review_id= Review.objects.values().first()['id']

    def test_client_is_foreignkey(self):
        review=Review.objects.get(id=self.review_id)
        client = review._meta.get_field('client')
        self.assertEquals(type(client),ForeignKey)
    def test_counselor_is_foreignkey(self):
        review=Review.objects.get(id=self.review_id)
        counselor = review._meta.get_field('counselor')
        self.assertEquals(type(counselor),ForeignKey)

   
    def test_content_max_length(self):
        review = Review.objects.get(id=self.review_id)
        max_length = review._meta.get_field('content').max_length
        self.assertEquals(max_length, 1000)

    def test_review_meta_verbose_name(self):
        review = Review.objects.all().first()
        self.assertEquals('후기', review._meta.verbose_name)
        
class ReviewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.review = Review()
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )
   
        client1 =self.user
        self.review=Review.objects.create(
            client=client1,
            counselor=client1,
            content="너무좋았어요"
        )
        self.review=Review.objects.create(
            client=client1,
            counselor=client1,
            content="너무좋았어요"
        )
        self.review_id= Review.objects.values().first()['id']

    def setUp(self):
        token, created = Token.objects.get_or_create(user=self.user)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)


    # 리뷰 업로드 test
    def test_A_review_upload(self):
        
        review_info ={
            "counselor":"super@gmail.com",
            "content":"test review content",
        }

        response= self.client.post('/reviews/',data=review_info)
        self.assertEqual(response.status_code,201)
    # 리뷰 수정 test
    def test_B_review_update(self):
        review_info={
            "review_id":self.review_id,
            "content" :" 수정됨 " 
        }
        
        response= self.client.put('/reviews/',data=json.dumps(review_info),content_type='application/json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data ,'Review updated success')

    #리뷰 삭제 test
    def test_C_review_delete(self):
        
        kwargs=str(self.review_id)
        response= self.client.delete('/reviews/'+kwargs+'/',content_type='application/json')
        self.assertEqual(response.status_code,200)



class GETReviewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.review = Review()
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )
   
        client1 =self.user
        self.review=Review.objects.create(
            client=client1,
            counselor=client1,
            content="너무좋았어요"
        )
        self.review=Review.objects.create(
            client=client1,
            counselor=client1,
            content="너무좋았어요"
        )
        self.review_id= Review.objects.values().first()['id']

    def setUp(self):
        token, created = Token.objects.get_or_create(user=self.user)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_review_by_client(self):
        url="/reviews/counselors/"
        kwargs=Review.objects.values().first()['client_id']
        response= self.client.get(url+str(kwargs)+'/',content_type='application/json')
        self.assertEqual(response.status_code,200)

        
    def test_get_review_by_client(self):
        url="/reviews/clients/"
        kwargs=Review.objects.values().first()['counselor_id']
        response= self.client.get(url+str(kwargs)+'/',content_type='application/json')
        self.assertEqual(response.status_code,200)
import sys
sys.path.append("..")
import json 

from django.test import TestCase,Client
from .models import Diary
from users.models import User
from rest_framework.authtoken.models import Token


# test용 데이터
class DiaryWordCloudTest(TestCase):

    def setUp(self):
        self.diary = Diary()
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )
        token, created = Token.objects.get_or_create(user=self.user)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        
    #순서제공
    def test_review_upload_AND_update_AND_delete(self):
        self.Test_text_extract_wordcloud_post
        # self.Test_text_extract_wordcloud_get
        # self.Test_text_extract_wordcloud_delete

    # 다이어리 업로드 + 워드클라우드 생성 test
    def Test_text_extract_wordcloud_post(self):
        url = '/diaries/'          
        dairy_data = { 
            'title':'오늘의 할일',
            'content':'테스트 드리븐 개발은 나를 성장시켜주고 새로운 것을 배우게 도와주는 즐거운 일이다. 어렵고 복잡하지만, 잘 이겨내서 좋은 개발자가 될것이다.'
        }
        response= self.client.post('url',data=dairy_data)
        print(response.data.content,dairy_data.content+"1")
        self.assertEquals(response.data.content,dairy_data.content+"1")

        self.assertEquals(response.status_code,201)
        self.assertEquals(response.data.title,dairy_data.title)
    # 다이어리 워드클라우드 가져오기 test
    def Test_text_extract_wordcloud_get(self):
        response= self.client.get('/reviews/'+kwargs+'/',content_type='application/json')
        self.assertEqual(response.status_code,201)

    # 다이어리 삭제 test
    def Test_text_extract_wordcloud_delete(self):
        response= self.client.delete('/reviews/'+kwargs+'/',content_type='application/json')
        self.assertEqual(response.status_code,200)

    def tearDown(self):
        # Clean up after each test
        self.user.delete()
        self.review.delete()
class LineGraphTest(TestCase):


    # 다이어리 업로드 + 워드클라우드 생성 test
    def Test_text_extract_linegraph_post(self):
        
        response= self.client.post('/',data=review_info)
        self.assertEqual(response.status_code,201)
    # 다이어리 워드클라우드 가져오기 test
    def Test_text_extract_linegraph_get(self):

        response= self.client.get('/reviews/'+kwargs+'/',content_type='application/json')
        self.assertEqual(response.status_code,201)

class WholeContentTest(TestCase):


    # 다이어리 업로드 + 워드클라우드 생성 test
    def Test_whole_content_post(self):
        
        response= self.client.post('/',data=review_info)
        self.assertEqual(response.status_code,201)
    # 다이어리 워드클라우드 가져오기 test
    def Test_whole_content_get(self):

        response= self.client.get('/reviews/'+kwargs+'/',content_type='application/json')
        self.assertEqual(response.status_code,201)
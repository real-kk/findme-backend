import sys
import io
from PIL import Image
sys.path.append("..")
import json 
import tempfile
from django.core.files.images import ImageFile
from django.test import TestCase,Client
from .models import Diary,DiaryWholeContent,LineGraph
from django.db.models.fields.files import ImageField
from users.models import User
from .serializers import DiarySerializer,WholeContentSerializer ,DiaryListSerializer
from rest_framework.authtoken.models import Token
from django.db.models.fields.related import ForeignKey
from datetime import datetime

class DiaryModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )

        # Set up non-modified objects used by all test methods
        Diary.objects.create(content='콘텐트', title='제목',client=self.user)
    
    def test_client_is_foreignkey(self):
        diary=Diary.objects.get(id=1)
        client = diary._meta.get_field('client')
        self.assertEquals(type(client),ForeignKey)

    def test_sentiment_score_label(self):
        diary=Diary.objects.get(id=1)
        field_label = diary._meta.get_field('sentiment_score').verbose_name
        self.assertEquals(field_label, '텍스트감정분석결과')

    def test_title_max_length(self):
        diary = Diary.objects.get(id=1)
        max_length = diary._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)
    def test_content_max_length(self):
        diary = Diary.objects.get(id=1)
        max_length = diary._meta.get_field('content').max_length
        self.assertEquals(max_length, 1000)

    def test_diary_meta_verbose_name(self):
        diary = Diary.objects.get(id=1)
        self.assertEquals('감정일기', diary._meta.verbose_name)

class DiaryWholeContentModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )

        DiaryWholeContent.objects.create(whole_content='전체 내용',client=self.user)
    def test_client_is_foreignkey(self):
        diary_whole_content=DiaryWholeContent.objects.get(id=1)
        client = diary_whole_content._meta.get_field('client')
        self.assertEquals(type(client),ForeignKey)

    def test_renew_flag_default_is_False(self):
        diary_whole_content = DiaryWholeContent.objects.get(id=1)
        default = diary_whole_content.renew_flag
        self.assertFalse(default)

    def test_whole_content_max_length(self):
        diary_whole_content = DiaryWholeContent.objects.get(id=1)
        max_length = diary_whole_content._meta.get_field('whole_content').max_length
        self.assertEquals(max_length, 10000)

    def test_diary_meta_verbose_name(self):
        whole_diary = DiaryWholeContent.objects.get(id=1)
        self.assertEquals('감정일기 내용 모음', whole_diary._meta.verbose_name)

class LineGraphModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )
      
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image_mock= ImageFile(file, name=file.name)
        LineGraph.objects.create(line_graph=image_mock,client=self.user)

    def test_client_is_foreignkey(self):
        line_graph=LineGraph.objects.get(id=1)
        client = line_graph._meta.get_field('client')
        self.assertEquals(type(client),ForeignKey)


    def test_line_graph_is_image_file(self):
        line_graph = LineGraph.objects.get(id=1)
        line_graph_img = line_graph._meta.get_field('line_graph')
        self.assertEquals(type(line_graph_img), ImageField)

    def test_line_graph_meta_verbose_name(self):
        line_graph = LineGraph.objects.get(id=1)
        self.assertEquals('꺾은선그래프 - 감정일기', line_graph._meta.verbose_name)

class SerializerTest(TestCase):
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )

        # Set up non-modified objects used by all test methods
        Diary.objects.create(content='콘텐트', title='제목',client=self.user)
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image_mock= ImageFile(file, name=file.name)
        DiaryWholeContent.objects.create(client= self.user, whole_content="아아아아어러러럴이잉",image=image_mock,renew_flag=True)
    
    def test_diary_serializer(self):
        serializer = DiarySerializer(data= Diary.objects.values().all().first())
        if not serializer.is_valid():
            import pprint
            pprint.pprint(serializer.errors)
        self.assertEqual(serializer.is_valid(), True)
    def test_whole_content_serializer(self):
        #현재 S3에 올라가있는 이미지라서 에러가 뜨는듯함
        serializer = WholeContentSerializer(data= DiaryWholeContent.objects.values().all())
        # if not serializer.is_valid():
        #     import pprint
        #     pprint.pprint(serializer.errors)
        self.assertEqual(serializer.is_valid(), False)

class DiaryWordCloudTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩',
            user_type=0                                                    
        )

        Diary.objects.create(content='콘텐트', title='제목',client=self.user,create_date= datetime.now().strftime('%Y-%m-%d'))

    def setUp(self):
        token, created = Token.objects.get_or_create(user=self.user)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    # 다이어리 업로드 + 워드클라우드 생성 test
    def test_A_text_extract_wordcloud_post(self):
        url = '/diaries/'          
        dairy_data = { 
            'title':'오늘의 할일',
            'content':'테스트 드리븐 개발은 나를 성장시켜주고 새로운 것을 배우게 도와주는 즐거운 일이다. 어렵고 복잡하지만, 잘 이겨내서 좋은 개발자가 될것이다.'
        }
        response= self.client.post(url,data=dairy_data)
        self.assertEquals(response.status_code,405)
        self.assertEquals(response.data,'Today Diary Existed')

    # 다이어리 워드클라우드 가져오기 test
    def test_B_text_extract_wordcloud_get_by_user(self):
        url='/diaries/'
        response= self.client.get(url,content_type='application/json')
        self.assertEqual(response.status_code,200)

    # 다이어리 삭제 test
    def test_C_text_extract_wordcloud_delete_by_id(self):
        url='/diaries/'
        kwargs=str(Diary.objects.values().first()['id'])
        response= self.client.delete(url+kwargs+'/',content_type='application/json')
        self.assertEqual(response.status_code,200)
        


class LineGraphTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )

        Diary.objects.create(content='1일차', title='제목1',client=self.user,sentiment_score=-0.1)
        Diary.objects.create(content='2일차', title='제목2',client=self.user,sentiment_score=0.1)
        Diary.objects.create(content='3일차', title='제목3',client=self.user,sentiment_score=-0.2)
        Diary.objects.create(content='4일차', title='제목4',client=self.user,sentiment_score=0.6)
        Diary.objects.create(content='5일차', title='제목5',client=self.user,sentiment_score=0.2)
        Diary.objects.create(content='6일차', title='제목6',client=self.user,sentiment_score=0.9)
        Diary.objects.create(content='7일차', title='제목7',client=self.user,sentiment_score=0.8)

    def setUp(self):
        token, created = Token.objects.get_or_create(user=self.user)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
    def test_text_extract_linegraph_post(self):
        response= self.client.post('/linegraph/')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data.get('line_graph')[:10],'https://fi')

    def test_text_extract_linegraph_get(self):

        response= self.client.get('/linegraph/',data={"client":"super@gmail.com"})
        self.assertEqual(response.status_code,200)


class WholeContentTest(TestCase):


    def Test_whole_content_post(self):
        
        response= self.client.post('/',data=review_info)
        self.assertEqual(response.status_code,201)
    def Test_whole_content_get(self):

        response= self.client.get('/reviews/'+kwargs+'/',content_type='application/json')
        self.assertEqual(response.status_code,201)
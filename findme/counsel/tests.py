from django.test import TestCase,Client
from users.models import User
from .models import Counsel,RegisterCounselDate
from .serializer import CounselSerializer,CounselListSerializer,CounselDateSerializer
from django.db.models.fields.files import ImageField
from rest_framework.authtoken.models import Token
from django.db.models.fields.related import ForeignKey
from django.core.files.images import ImageFile
import tempfile
import json 
import io
from PIL import Image
from datetime import datetime

class CounselModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(                                   
            email='super@gmail.com',                                                                   
            password='test',
            username='강낭콩'                                                    
        )
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image_mock= ImageFile(file, name=file.name)
        # Set up non-modified objects used by all test methods
        Counsel.objects.create(client=self.user,counselor=self.user,time_table=image_mock,
        major='소프트',student_number='201211222',phone_number='01031332322',content='신청합니다')
        self.counsel_id = Counsel.objects.values().first()['id']
    def test_client_is_foreignkey(self):
        counsel=Counsel.objects.get(id=self.counsel_id)
        client = counsel._meta.get_field('client')
        self.assertEquals(type(client),ForeignKey)
    def test_counselor_is_foreignkey(self):
        counsel=Counsel.objects.get(id=self.counsel_id)
        counselor = counsel._meta.get_field('counselor')
        self.assertEquals(type(counselor),ForeignKey)

    def test_max_length(self):
        counsel=Counsel.objects.get(id=self.counsel_id)
        max_length = counsel._meta.get_field('major').max_length
        self.assertEquals(max_length, 100)
        max_length = counsel._meta.get_field('student_number').max_length
        self.assertEquals(max_length, 100)
        
        max_length = counsel._meta.get_field('phone_number').max_length
        self.assertEquals(max_length, 100)
        max_length = counsel._meta.get_field('content').max_length
        self.assertEquals(max_length, 100)
        
    def test_diary_meta_verbose_name(self):
        counsel=Counsel.objects.get(id=self.counsel_id)
        self.assertEquals('신청서', counsel._meta.verbose_name)



class SerializerTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user_client = User.objects.create(                                   
            email='user1@gmail.com',                                                                   
            password='test',
            username='난상담',
            user_type=1                                               
        )
        self.user_counselor = User.objects.create(                                   
            email='user0@gmail.com',                                                                   
            password='test',
            username='난내담',
            user_type=0
        )                                             
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image_mock= ImageFile(file, name=file.name)

        # Set up non-modified objects used by all test methods
        Counsel.objects.create(client=self.user_client,counselor=self.user_counselor,time_table=image_mock,
        major='소프트',student_number='201211222',phone_number='01031332322',content='신청합니다')
        RegisterCounselDate.objects.create(client=self.user_client,counselor=self.user_counselor)
        self.counsel_id = Counsel.objects.values().first()['id']

    def test_counsel_serializer(self):
        serializer = CounselSerializer(data=Counsel.objects.values().all().first())
        if not serializer.is_valid():
            import pprint
            pprint.pprint(serializer.errors)
        self.assertEqual(serializer.is_valid(), True)
    def test_counsel_list_serializer(self):
        counsel = Counsel.objects.all()
        serializer = CounselListSerializer( counsel, many=True)
    def test_counsel_date_serializer(self): 
        serializer = CounselDateSerializer(data=RegisterCounselDate.objects.values().all().first())
        if not serializer.is_valid():
            import pprint
            pprint.pprint(serializer.errors)
        self.assertEqual(serializer.is_valid(), True)
class CounselApplicationTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user_client = User.objects.create(                                   
            email='user1@gmail.com',                                                                   
            password='test',
            username='난상담',
            user_type=1                                               
        )
        self.user_counselor = User.objects.create(                                   
            email='user0@gmail.com',                                                                   
            password='test',
            username='난내담',
            user_type=0
        )                                             
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image_mock= ImageFile(file, name=file.name)

        # Set up non-modified objects used by all test methods
        Counsel.objects.create(client=self.user_client,counselor=self.user_counselor,time_table=image_mock,
        major='소프트',student_number='201211222',phone_number='01031332322',content='신청합니다')
        self.counsel_id = Counsel.objects.values().first()['id']
    
    def setUp(self):
        token, created = Token.objects.get_or_create(user=self.user_client)                
        # token, created = Token.objects.get_or_create(user=self.user_counselor)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    # 상담 신청서 업로드 test
    def test_A_text_application_post(self):
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image_mock= ImageFile(file, name=file.name)

        url = '/counsels/'          
        counsels_data = { 
            'client':self.user_client,
            'counselor':self.user_counselor,
            'major':'공부나할과',
            'student_number':'201512151',
            'phone_number':'01099999999',
            'content':'테스트 드리븐 개발은 나를 성장시켜주고 새로운 것을 배우게 도와주는 즐거운 일이다. 어렵고 복잡하지만, 잘 이겨내서 좋은 개발자가 될것이다.'
        }
        response= self.client.post(url,data=counsels_data)
        self.assertEquals(response.status_code,201)

    # 상담 신청서 가져오기 test
    def test_B_text_application_get(self):
        url='/counsels/'
        response= self.client.get(url,content_type='application/json')
        self.assertEqual(response.status_code,200)
    
    # 상담 신청서 수정 test
    def test_C_text_application_put(self):
        url='/counsels/'
        
        counsels_data = { 
            'client':self.user_client.email,
            'counselor':self.user_counselor.email,
            'major':'공부나할과',
            'student_number':'201512151',
            'phone_number':'01099999999',
            'content':'테스트 드리븐 개발은 나를 성장시켜주고 새로운 것을 배우게 도와주는 즐거운 일이다. 어렵고 복잡하지만, 잘 이겨내서 좋은 개발자가 될것이다.'
        }
        kwargs="1"
        response= self.client.put(url+kwargs+'/',data=json.dumps(counsels_data),content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data,'Counsel was updated')



    # 상담 신청서 삭제 test
    def test_D_text_application_delete(self):
        url='/counsels/'
        kwargs="1"
        response= self.client.delete(url+kwargs+'/',content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data,'Counsel was deleted')


class CounselPhotoTest(TestCase):
    
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
    @classmethod
    def setUpTestData(self):
        self.user_client = User.objects.create(                                   
            email='user1@gmail.com',                                                                   
            password='test',
            username='난상담',
            user_type=1                                               
        )
        self.user_counselor = User.objects.create(                                   
            email='user0@gmail.com',                                                                   
            password='test',
            username='난내담',
            user_type=0
        )                                             
        file = tempfile.NamedTemporaryFile(suffix='.png')
        image_mock= ImageFile(file, name=file.name)

        # Set up non-modified objects used by all test methods
        Counsel.objects.create(client=self.user_client,counselor=self.user_counselor,time_table=image_mock,
        major='소프트',student_number='201211222',phone_number='01031332322',content='신청합니다')
        self.counsel_id = Counsel.objects.values().first()['id']
    
    def setUp(self):
        token, created = Token.objects.get_or_create(user=self.user_client)                
        # token, created = Token.objects.get_or_create(user=self.user_counselor)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    # 상담 신청서 업로드 test
    def test_A_counsel_photo_add(self):
        photo_file = self.generate_photo_file()
        print(photo_file)
        kwargs=str(Counsel.objects.values().first()["id"])
        url = '/counsels/photo/'+kwargs+'/'
        data={
            'time_table': photo_file
        }
        response= self.client.post(url,data,format='multipart')
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data,"Counsel time table was updated")



class CounselDateTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user_client = User.objects.create(                                   
            email='user1@gmail.com',                                                                   
            password='test',
            username='난상담',
            user_type=1                                               
        )
        self.user_counselor = User.objects.create(                                   
            email='user0@gmail.com',                                                                   
            password='test',
            username='난내담',
            user_type=0
        )                                             

    def setUp(self):
        RegisterCounselDate.objects.create(client=self.user_client,counselor=self.user_counselor)

        token, created = Token.objects.get_or_create(user=self.user_counselor)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    # 상담 등록 test
    def test_A_counsel_date_add(self):
        url='/counsels/date/'
        data={
            'client':self.user_counselor.email,
            'counsel_date':datetime.now()
        }
        response= self.client.post(url,data=data)       
        self.assertEqual(response.status_code,201)
    #등록된 상담 조회 test
    def test_B_counsel_date_get(self):
        url='/counsels/date/'
        response = self.client.get(url)       
        self.assertEqual(response.status_code,200)

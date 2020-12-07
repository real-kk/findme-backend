from django.test import TestCase
import mock
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase,Client
from users.models import User
from .models import Task
from .serializers import TaskSerializer,TaskQuestionSerializer
from django.db.models.fields.files import ImageField
from rest_framework.authtoken.models import Token
from django.db.models.fields.related import ForeignKey
from django.core.files.images import ImageFile
import tempfile
from django.db.models.fields.files import FileField
import json 
from PIL import Image
from datetime import datetime
from django.db.models.fields import FloatField
class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user_counselor = User.objects.create(                                   
            email='super1@gmail.com',                                                                   
            password='test',
            username='김상담',
            user_type=1                                                    
        )
        self.user_client = User.objects.create(                                   
            email='super2@gmail.com',                                                                   
            password='test',
            username='김내담',
            user_type=1                                                    
        )
        self.video = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")

        Task.objects.create(client=self.user_client,counselor=self.user_counselor,question="질문")
        self.task_id = Task.objects.values().first()['id']
    def test_client_is_foreignkey(self):
        task=Task.objects.get(id=self.task_id)
        client = task._meta.get_field('client')
        self.assertEquals(type(client),ForeignKey)
    def test_counselor_is_foreignkey(self):
        task=Task.objects.get(id=self.task_id)
        counselor = task._meta.get_field('counselor')
        self.assertEquals(type(counselor),ForeignKey)




class SerializerTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user_counselor = User.objects.create(                                   
            email='super1@gmail.com',                                                                   
            password='test',
            username='김상담',
            user_type=1                                                    
        )
        self.user_client = User.objects.create(                                   
            email='super2@gmail.com',                                                                   
            password='test',
            username='김내담',
            user_type=1                                                    
        )
        self.video = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")

        Task.objects.create(client=self.user_client,counselor=self.user_counselor,question="질문")
        self.task_id = Task.objects.values().first()['id']

    def test_task_serializer(self):
        serializer = TaskSerializer(Task.objects.values().all().first()['video'])
    #어렵다..




class TaskQuestionTest(TestCase):
    def setUp(self):
        self.user_counselor = User.objects.create(                                   
            email='super1@gmail.com',                                                                   
            password='test',
            username='김상담',
            user_type=1                                                    
        )
        self.user_client = User.objects.create(                                   
            email='super2@gmail.com',                                                                   
            password='test',
            username='김내담',
            user_type=1                                                    
        )
        Task.objects.create(client=self.user_client,counselor=self.user_counselor,question="질문")

        token, created = Token.objects.get_or_create(user=self.user_counselor)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        
    def test_a_task_question_upload(self):
        url = '/tasks/questions/'
        data={
            "client":self.user_client.email,
            "question": "질문입니다."
        }
        response =self.client.post(url,data=data)
        self.assertEqual(response.status_code,201)

    def test_b_task_question_get(self):
        url = '/tasks/questions/'
        response =self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_c_task_question_for_counselor_get(self):
        url = "/tasks/questions_counselor/?client="+self.user_client.email
        response =self.client.get(url)
        self.assertEqual(response.status_code,200)


class TaskVideoTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user_counselor = User.objects.create(                                   
            email='super1@gmail.com',                                                                   
            password='test',
            username='김상담',
            user_type=1                                                    
        )
        self.user_client = User.objects.create(                                   
            email='super2@gmail.com',                                                                   
            password='test',
            username='김내담',
            user_type=1                                                    
        )

        Task.objects.create(client=self.user_client,counselor=self.user_counselor,question="질문")
        self.task_id = Task.objects.values().first()['id']

    def setUp(self):
        token, created = Token.objects.get_or_create(user=self.user_client)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_a_task_question_get(self):
        url = '/tasks/questions/'
        response =self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_b_task_video_upload(self):
        url = "/tasks/videos/"+str(self.task_id) + "/022db29c-d0e2-11e5-bb4c-60f81dca7676/"
        self.video = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        response =self.client.post(url,data={"video":self.video})
        self.assertEqual(response.status_code,201)

    def test_c_task_video_processing_upload(self):
        url ="/tasks/process_videos/"+str(self.task_id)+"/"
        response =self.client.get(url)
        self.assertEqual("https://processed-video-lambda." in response.data,True)
        self.assertEqual(response.status_code,200)

        
    def test_d_task_video_delete(self):
        task_id = Task.objects.values().first()['id']
        url = '/tasks/'+str(task_id)+"/"
        response =self.client.delete(url)
        self.assertEqual(response.status_code,200)


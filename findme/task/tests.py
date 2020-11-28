from django.test import TestCase

from django.test import TestCase,Client
from users.models import User
from .models import Task
from .serializers import TaskSerializer,TaskQuestionSerializer
from django.db.models.fields.files import ImageField
from rest_framework.authtoken.models import Token
from django.db.models.fields.related import ForeignKey
from django.core.files.images import ImageFile
import tempfile
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

        Task.objects.create(client=self.user_client,counselor=self.user_counselor,video=self.video,question="질문",anger='0.111',disgust='0.111',fear='0.131',happiness='0.414',neutral='0.01',sadness='0.34',surprise='0.13')
        self.task_id = Task.objects.values().first()['id']
    def test_client_is_foreignkey(self):
        task=Task.objects.get(id=self.task_id)
        client = task._meta.get_field('client')
        self.assertEquals(type(client),ForeignKey)
    def test_counselor_is_foreignkey(self):
        task=Task.objects.get(id=self.task_id)
        counselor = task._meta.get_field('counselor')
        self.assertEquals(type(counselor),ForeignKey)

    def test_is_float(self):
        task=Task.objects.get(id=self.task_id)
        column = task._meta.get_field('anger')
        self.assertEquals(type(column),FloatField)
        column = task._meta.get_field('disgust')
        self.assertEquals(type(column),FloatField)
        column = task._meta.get_field('fear')
        self.assertEquals(type(column),FloatField)
        column = task._meta.get_field('happiness')
        self.assertEquals(type(column),FloatField)
        column = task._meta.get_field('neutral')
        self.assertEquals(type(column),FloatField)
        column = task._meta.get_field('sadness')
        self.assertEquals(type(column),FloatField)
        column = task._meta.get_field('surprise')
        self.assertEquals(type(column),FloatField)


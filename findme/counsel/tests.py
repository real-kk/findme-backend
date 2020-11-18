from django.test import TestCase
from users.models import User
from .models import Counsel

from django.db.models.fields.files import ImageField
from rest_framework.authtoken.models import Token
from django.db.models.fields.related import ForeignKey
from django.core.files.images import ImageFile
import tempfile

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
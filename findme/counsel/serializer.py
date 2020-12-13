from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Counsel, RegisterCounselDate
class CounselSerializer(serializers.Serializer):
    id = ReadOnlyField()
    client_username = ReadOnlyField(source="client.username")
    counselor_username = ReadOnlyField(source="counselor.username")
    major = serializers.CharField(max_length=100)
    student_number = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)
    create_date = serializers.DateTimeField(allow_null=True)
    content = serializers.CharField(max_length=100)
    class Meta:
        model = Counsel
        fields = ('id', 'student_number', 'phone_number', 'client_username', 'create_date' 'counselor_username', 'major', 'content')

class CounselPhotoSerializer(serializers.Serializer):
    time_table = serializers.ImageField(use_url=True, allow_null=True)
    class Meta:
        model = Counsel
        fields = ('time_table')

class CounselListSerializer(serializers.Serializer):
    id = ReadOnlyField()
    counselor_username= ReadOnlyField(source="counselor.username")
    counselor_email = ReadOnlyField(source='counselor.email')
    client_image = ReadOnlyField(source='client.image.name')
    client_username = ReadOnlyField(source="client.username")
    client_introduce = ReadOnlyField(source="client.introduce")
    client_email = ReadOnlyField(source='client.email')
    major = serializers.CharField(max_length=100)
    student_number = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)
    time_table = serializers.ImageField(use_url=True,allow_null=True)
    create_date = serializers.DateTimeField(allow_null=True)
    content = serializers.CharField(max_length=100)
    class Meta:
        model = Counsel
        fields = ('id','counselor_username','counselor_email','student_number', 'phone_number', 'time_table', 'client_email','client_username', 'create_date', 'counselor_username', 'major', 'content')
            
class CounselDateSerializer(serializers.Serializer):
    counselor_username = ReadOnlyField(source="counselor.username")
    client_username = ReadOnlyField(source="client.username")

    class Meta:
        model = RegisterCounselDate
        fields = ('counselor_username', 'client_username')

class CounselClientSerializer(serializers.Serializer):
    client_username = ReadOnlyField(source="client.username")
    client_email = ReadOnlyField(source="client.email")
    client_image = ReadOnlyField(source="client.image.name")
    client_introduce = ReadOnlyField(source="client.introduce")
    major = serializers.CharField(max_length=100)
    student_number = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)
    time_table = serializers.ImageField(use_url=True,allow_null=True)
    create_date = serializers.DateTimeField(allow_null=True)
    content = serializers.CharField(max_length=100)

    class Meta:
        model = RegisterCounselDate
        fields = ('client_username', 'client','client_image','client_introduce','major','student_number','phone_number','time_table','content')

class CounselCounselorSerializer(serializers.Serializer):
    counselor_username = ReadOnlyField(source="counselor.username")
    counselor_email = ReadOnlyField(source="counselor.email")

    class Meta:
        model = RegisterCounselDate
        fields = ('counselor_username', 'counselor_email')

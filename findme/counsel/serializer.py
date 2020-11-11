from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Counsel, RegisterCounselDate
class CounselSerializer(serializers.Serializer):
    client_username = ReadOnlyField(source="client.username")
    counselor_username = ReadOnlyField(source="counselor.username")
    major = serializers.CharField(max_length=100)
    student_number = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)
    time_table = serializers.ImageField(use_url=True,allow_null=True)
    create_date = serializers.DateTimeField(allow_null=True)
    content = serializers.CharField(max_length=100)
    class Meta:
        model = Counsel
        fields = ('student_number', 'phone_number', 'time_table', 'client_username', 'create_date' 'counselor_username', 'major', 'content')
            
class CounselListSerializer(serializers.Serializer):
    client_username = ReadOnlyField(source="client.username")
    client_email = ReadOnlyField(source='client.email')
    major = serializers.CharField(max_length=100)
    student_number = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)
    time_table = serializers.ImageField(use_url=True,allow_null=True)
    create_date = serializers.DateTimeField(allow_null=True)
    content = serializers.CharField(max_length=100)
    class Meta:
        model = Counsel
        fields = ('student_number', 'phone_number', 'time_table', 'client_email','client_username', 'create_date', 'counselor_username', 'major', 'content')
            
class CounselDateSerializer(serializers.Serializer):
    counselor_username = ReadOnlyField(source="counselor.username")
    client = ReadOnlyField(source="client.email")
   # counsel_date = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = RegisterCounselDate
        fields = ('counselor_username', 'client')#, 'counsel_date')

class CounselClientSerializer(serializers.Serializer):
    client_username = ReadOnlyField(source="client.username")
    class Meta:
        model = RegisterCounselDate
        fields = ('client_username',)

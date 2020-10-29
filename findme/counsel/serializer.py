from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Counsel, CounselDate
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
    major = serializers.CharField(max_length=100)
    student_number = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)
    time_table = serializers.ImageField(use_url=True,allow_null=True)
    create_date = serializers.DateTimeField(allow_null=True)
    content = serializers.CharField(max_length=100)
    class Meta:
        model = Counsel
        fields = ('student_number', 'phone_number', 'time_table', 'client_username', 'create_date', 'counselor_username', 'major', 'content')
            
class CounselDateSerializer(serializers.Serializer):
    counselor_username = ReadOnlyField(source="counselor.username")
    client_username = ReadOnlyField(source="client.username")
    counsel_date = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = CounselDate
        fields = ('counselor_username', 'client_username', 'counsel_date')
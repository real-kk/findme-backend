from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,ReadOnlyField
from .models import  Task


class TaskSerializer(serializers.ModelSerializer):
    client_username = ReadOnlyField(source="client.username")
    video = serializers.FileField(use_url=True,allow_null=False)

    class Meta:
        model = Task
        fields = ['title','video','client_username'] 
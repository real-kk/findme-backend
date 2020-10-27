from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,ReadOnlyField
from .models import  Task


class TaskSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=True,allow_null=True)
    client_username = ReadOnlyField(source="client.username")

    class Meta:
        model = Task
        fields =('title','client_username','create_date','video')
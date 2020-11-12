from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,ReadOnlyField
from .models import  Task, TaskQuestion


class TaskSerializer(serializers.ModelSerializer):
    client_username = ReadOnlyField(source="client.username")
    video = serializers.FileField(use_url=True,allow_null=False)
    class Meta:
        model = Task
        fields = ['video', 'client_username']
        
class TaskQuestionSerializer(serializers.ModelSerializer):
    client_email = ReadOnlyField(source="client.email")
    counselor_username = ReadOnlyField(source="counselor.username")

    class Meta:
        model = TaskQuestion
        fields = ['question', 'client_email', 'counselor_username']
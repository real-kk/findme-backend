from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,ReadOnlyField
from .models import  Task


class TaskSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=True,allow_null=False)
    task_id =serializers.IntegerField()
    class Meta:
        model = Task
        fields = ['video' ,'task_id']
class TaskQuestionSerializer(serializers.ModelSerializer):
    client_email = ReadOnlyField(source="client.email")
    counselor_username = ReadOnlyField(source="counselor.username")
    question = serializers.CharField(max_length=100)

    class Meta:
        model = Task
        fields = ['question', 'client_email', 'counselor_username']

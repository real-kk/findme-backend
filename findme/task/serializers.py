from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,ReadOnlyField
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=True,allow_null=False)
    class Meta:
        model = Task
        fields = ['video']
class TaskQuestionSerializer(serializers.ModelSerializer):
    id = ReadOnlyField()
    client_email = ReadOnlyField(source="client.email")
    counselor_username = ReadOnlyField(source="counselor.username")
    counselor_image = ReadOnlyField(source="counselor.image.name")
    question = serializers.CharField(max_length=100)

    class Meta:
        model = Task
        fields = ['id', 'question', 'client_email', 'counselor_username','counselor_image']

class SentimentGraphSerializer(serializers.ModelSerializer):
    client_username = ReadOnlyField(source="client.username")
    graph = serializers.ImageField(use_url=True, allow_null=True)

    class Meta:
        model = Task
        fields = ('client_username', 'graph')

from rest_framework import serializers
from .models import Diary
from rest_framework.serializers import ModelSerializer, ReadOnlyField


class DiarySerializer(serializers.ModelSerializer):
    client_username = ReadOnlyField(source="client.username")
    class Meta:
        model = Diary
        fields = ('title', 'client_username', 'create_date', 'content')
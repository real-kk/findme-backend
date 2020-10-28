from rest_framework import serializers
from .models import Diary
from rest_framework.serializers import ModelSerializer, ReadOnlyField
import datetime
from pytz import timezone


class DiarySerializer(serializers.ModelSerializer):
    client_username = ReadOnlyField(source="client.username")
    class Meta:
        model = Diary
        fields = ('title', 'client_username', 'create_date', 'content')


class DiaryListSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()

    def get_create_date(self, obj):
        return obj.create_date.astimezone(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M')
    class Meta:
        model = Diary
        fields = ('title', 'create_date', 'content', 'sentiment_score')

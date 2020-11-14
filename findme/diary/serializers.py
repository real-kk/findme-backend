from rest_framework import serializers
from .models import Diary, DiaryWholeContent, LineGraph
from rest_framework.serializers import ModelSerializer, ReadOnlyField
import datetime
from pytz import timezone


class DiarySerializer(serializers.ModelSerializer):
    client_username = ReadOnlyField(source="client.username")
    class Meta:
        model = Diary
        fields = ('title', 'client_username', 'create_date', 'content')


class DiaryListSerializer(serializers.ModelSerializer):
    id = ReadOnlyField()

    create_date = serializers.SerializerMethodField()

    def get_create_date(self, obj):
        return obj.create_date.astimezone(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M')
    class Meta:
        model = Diary
        fields = ('id','title', 'create_date', 'content')

class WholeContentSerializer(serializers.ModelSerializer):
    client_username = ReadOnlyField(source="client.username")
    class Meta:
        model = DiaryWholeContent
        fields = ('client_username', 'image')

class LineGraphSerializer(serializers.ModelSerializer):
    client_username = ReadOnlyField(source="client.username")

    class Meta:
        model = LineGraph
        fields = ('client_username', 'line_graph')
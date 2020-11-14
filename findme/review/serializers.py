from rest_framework import serializers
from .models import Review
from rest_framework.serializers import ModelSerializer,ReadOnlyField
from pytz import timezone

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    id = ReadOnlyField()

    create_date = serializers.SerializerMethodField()
    counselor_name= serializers.SerializerMethodField()
    client_name= serializers.SerializerMethodField()

    def get_counselor_name(self,obj):
        return obj.counselor.username

    def get_client_name(self,obj):
        return obj.client.username
        
    def get_create_date(self, obj):
        return obj.create_date.astimezone(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M')
    class Meta:
        model = Review
        fields = ('id','counselor_name','client_name', 'create_date', 'content')
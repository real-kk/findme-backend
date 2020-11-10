from rest_framework import serializers
from .models import Review
from rest_framework.serializers import ModelSerializer,ReadOnlyField

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
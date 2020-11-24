from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,ReadOnlyField
from .models import Voice

class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voice
        fields = ['voice']

from rest_framework import serializers
from .models import Review
from rest_framework.serializers import ModelSerializer


class ReviewSerializer(serializers.ModelSerializer):
    counselor_username = ReadOnlyField(source="counselor.username")
    client_username = ReadOnlyField(source="client.username")
    counsel_date = serializers.DateTimeField(allow_null=True)
    class Meta:
        model = Review
        fields = "__all__"
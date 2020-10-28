from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models  import Counsel
class CounselSerializer(serializers.Serializer):
        client_username = ReadOnlyField(source="client.username")
        counselor_username = ReadOnlyField(source="counselor.username")

        class Meta:
            model = Counsel
            fields = ('student_number','phone_number','time_table', 'client_username', 'counselor_username','create_date', 'major')
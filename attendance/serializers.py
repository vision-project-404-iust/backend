from rest_framework import serializers
from .models import StudentData


class StudentDataSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentData model
    """
    class Meta:
        model = StudentData
        fields = ['id', 'studentID', 'FramID', 'ClassID', 'Emotion', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

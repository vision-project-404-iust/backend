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


class StudentOverallStatusSerializer(serializers.Serializer):
    """
    Serializer for GetStudentOverallStatus API response
    """
    studentID = serializers.CharField()
    overall_status = serializers.CharField()
    total_classes = serializers.IntegerField()
    attended_classes = serializers.IntegerField()
    attendance_rate = serializers.FloatField()
    emotion_summary = serializers.DictField()


class ClassStatusSerializer(serializers.Serializer):
    """
    Serializer for GetClassStatus API response
    """
    ClassID = serializers.IntegerField()
    total_students = serializers.IntegerField()
    present_students = serializers.IntegerField()
    absent_students = serializers.IntegerField()
    attendance_rate = serializers.FloatField()
    emotion_distribution = serializers.DictField()
    students_list = serializers.ListField(child=serializers.DictField())

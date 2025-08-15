from django.db import models
from django.db.models import JSONField


class StudentData(models.Model):
    """
    Model to store student attendance and emotion data
    """
    studentID = models.CharField(max_length=50, verbose_name="Student ID")
    FramID = models.IntegerField(verbose_name="Frame ID")
    ClassID = models.IntegerField(verbose_name="Class ID")
    Emotion = JSONField(verbose_name="Emotion Data")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_data'
        verbose_name = "Student Data"
        verbose_name_plural = "Student Data"
        indexes = [
            models.Index(fields=['studentID']),
            models.Index(fields=['ClassID']),
            models.Index(fields=['FramID']),
        ]

    def __str__(self):
        return f"Student {self.studentID} - Class {self.ClassID} - Frame {self.FramID}"

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import StudentData
from .serializers import (
    StudentDataSerializer,
    StudentOverallStatusSerializer,
    ClassStatusSerializer
)


class GetStudentOverallStatus(APIView):
    """
    API endpoint to get overall status of a specific student
    """
    
    def get(self, request, student_id):
        """
        Get overall attendance and emotion status for a specific student
        
        Args:
            student_id (str): The student ID to get status for
            
        Returns:
            Response: Student overall status data
        """
        try:
            # TODO: Implement the logic to calculate student overall status
            # This should include:
            # - Total classes attended vs total classes
            # - Overall attendance rate
            # - Emotion summary across all classes
            # - Overall status (Excellent, Good, Fair, Poor)
            
            # Placeholder response - replace with actual logic
            response_data = {
                'studentID': student_id,
                'overall_status': 'Good',  # TODO: Calculate based on attendance and emotion
                'total_classes': 0,  # TODO: Count total classes
                'attended_classes': 0,  # TODO: Count attended classes
                'attendance_rate': 0.0,  # TODO: Calculate attendance rate
                'emotion_summary': {}  # TODO: Aggregate emotion data
            }
            
            serializer = StudentOverallStatusSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving student status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetClassStatus(APIView):
    """
    API endpoint to get status of a specific class
    """
    
    def get(self, request, class_id):
        """
        Get attendance and emotion status for a specific class
        
        Args:
            class_id (int): The class ID to get status for
            
        Returns:
            Response: Class status data
        """
        try:
            # TODO: Implement the logic to calculate class status
            # This should include:
            # - Total students in class
            # - Present vs absent students
            # - Class attendance rate
            # - Emotion distribution across students
            # - List of students with their individual status
            
            # Placeholder response - replace with actual logic
            response_data = {
                'ClassID': class_id,
                'total_students': 0,  # TODO: Count total students in class
                'present_students': 0,  # TODO: Count present students
                'absent_students': 0,  # TODO: Count absent students
                'attendance_rate': 0.0,  # TODO: Calculate class attendance rate
                'emotion_distribution': {},  # TODO: Aggregate emotion data
                'students_list': []  # TODO: List of students with their status
            }
            
            serializer = ClassStatusSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving class status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





# Additional utility views for development and testing
class StudentDataList(APIView):
    """
    List all student data records (for development/testing)
    """
    
    def get(self, request):
        students = StudentData.objects.all().order_by('-created_at')
        serializer = StudentDataSerializer(students, many=True)
        return Response(serializer.data)


class StudentDataDetail(APIView):
    """
    Retrieve a specific student data record (for development/testing)
    """
    
    def get(self, request, pk):
        student = get_object_or_404(StudentData, pk=pk)
        serializer = StudentDataSerializer(student)
        return Response(serializer.data)

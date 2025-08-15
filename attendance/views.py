from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
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
            # Get all records for the student
            student_records = StudentData.objects.filter(studentID=student_id)
            
            if not student_records.exists():
                return Response(
                    {'error': f'No records found for student {student_id}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Calculate total unique classes
            total_classes = student_records.values('ClassID').distinct().count()
            
            # Calculate attended classes (assuming presence in any frame means attendance)
            attended_classes = student_records.values('ClassID').distinct().count()
            
            # Calculate attendance rate
            attendance_rate = (attended_classes / total_classes * 100) if total_classes > 0 else 0.0
            
            # Aggregate emotion data across all records
            emotion_summary = {}
            for record in student_records:
                if isinstance(record.Emotion, dict):
                    for emotion, value in record.Emotion.items():
                        if emotion in emotion_summary:
                            emotion_summary[emotion] += value
                        else:
                            emotion_summary[emotion] = value
            
            # Calculate overall status based on attendance rate and emotion
            overall_status = self._calculate_overall_status(attendance_rate, emotion_summary)
            
            response_data = {
                'studentID': student_id,
                'overall_status': overall_status,
                'total_classes': total_classes,
                'attended_classes': attended_classes,
                'attendance_rate': round(attendance_rate, 2),
                'emotion_summary': emotion_summary
            }
            
            serializer = StudentOverallStatusSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving student status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _calculate_overall_status(self, attendance_rate, emotion_summary):
        """
        Calculate overall status based on attendance rate and emotion data
        """
        if attendance_rate >= 90:
            base_status = 'Excellent'
        elif attendance_rate >= 80:
            base_status = 'Good'
        elif attendance_rate >= 70:
            base_status = 'Fair'
        else:
            base_status = 'Poor'
        
        # Consider emotion data for final status
        if emotion_summary:
            # Calculate average positive emotions if they exist
            positive_emotions = ['happy', 'joy', 'excited', 'content', 'positive']
            negative_emotions = ['sad', 'angry', 'fear', 'disgust', 'negative']
            
            positive_score = sum(emotion_summary.get(emotion, 0) for emotion in positive_emotions)
            negative_score = sum(emotion_summary.get(emotion, 0) for emotion in negative_emotions)
            
            if positive_score > negative_score and positive_score > 0:
                if base_status == 'Poor':
                    return 'Fair'
                elif base_status == 'Fair':
                    return 'Good'
        
        return base_status


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
            # Get all records for the class
            class_records = StudentData.objects.filter(ClassID=class_id)
            
            if not class_records.exists():
                return Response(
                    {'error': f'No records found for class {class_id}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Calculate total unique students in class
            total_students = class_records.values('studentID').distinct().count()
            
            # Calculate present students (students who appear in any frame)
            present_students = class_records.values('studentID').distinct().count()
            
            # Calculate absent students (this would need additional logic based on expected students)
            # For now, assuming all students in records are present
            absent_students = 0
            
            # Calculate class attendance rate
            attendance_rate = (present_students / total_students * 100) if total_students > 0 else 0.0
            
            # Aggregate emotion distribution across all students in class
            emotion_distribution = {}
            for record in class_records:
                if isinstance(record.Emotion, dict):
                    for emotion, value in record.Emotion.items():
                        if emotion in emotion_distribution:
                            emotion_distribution[emotion] += value
                        else:
                            emotion_distribution[emotion] = value
            
            # Get list of students with their individual status
            students_list = []
            unique_students = class_records.values('studentID').distinct()
            
            for student_data in unique_students:
                student_id = student_data['studentID']
                student_records = class_records.filter(studentID=student_id)
                
                # Calculate student's emotion summary for this class
                student_emotion_summary = {}
                for record in student_records:
                    if isinstance(record.Emotion, dict):
                        for emotion, value in record.Emotion.items():
                            if emotion in student_emotion_summary:
                                student_emotion_summary[emotion] += value
                            else:
                                student_emotion_summary[emotion] = value
                
                # Calculate student's status for this class
                student_status = self._calculate_student_class_status(student_emotion_summary)
                
                students_list.append({
                    'studentID': student_id,
                    'status': student_status,
                    'emotion_summary': student_emotion_summary,
                    'frames_attended': student_records.count()
                })
            
            response_data = {
                'ClassID': class_id,
                'total_students': total_students,
                'present_students': present_students,
                'absent_students': absent_students,
                'attendance_rate': round(attendance_rate, 2),
                'emotion_distribution': emotion_distribution,
                'students_list': students_list
            }
            
            serializer = ClassStatusSerializer(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving class status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _calculate_student_class_status(self, emotion_summary):
        """
        Calculate student's status for a specific class based on emotion data
        """
        if not emotion_summary:
            return 'Unknown'
        
        # Calculate positive vs negative emotion scores
        positive_emotions = ['happy', 'joy', 'excited', 'content', 'positive']
        negative_emotions = ['sad', 'angry', 'fear', 'disgust', 'negative']
        
        positive_score = sum(emotion_summary.get(emotion, 0) for emotion in positive_emotions)
        negative_score = sum(emotion_summary.get(emotion, 0) for emotion in negative_emotions)
        
        if positive_score > negative_score and positive_score > 0:
            return 'Engaged'
        elif negative_score > positive_score and negative_score > 0:
            return 'Distracted'
        else:
            return 'Neutral'





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

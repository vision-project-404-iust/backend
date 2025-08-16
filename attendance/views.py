from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from .models import StudentData


class GetAttendanceStatus(APIView):
    """
    API endpoint to get attendance rate of all classIDs as a list
    """
    
    def get(self, request):
        """
        Get attendance rate for all classes
        
        Returns:
            Response: List of attendance rates for all classes
        """
        try:
            # Get all unique class IDs
            class_ids = StudentData.objects.values_list('ClassID', flat=True).distinct()
            
            attendance_data = []
            for class_id in class_ids:
                # Get all records for this class
                class_records = StudentData.objects.filter(ClassID=class_id)
                
                # Get unique students in this class
                unique_students = class_records.values('studentID').distinct()
                total_students = unique_students.count()
                
                # Calculate attendance rate
                attendance_rate = 0.0
                if total_students > 0:
                    # Count students who have any records (attended)
                    attended_students = unique_students.count()
                    attendance_rate = (attended_students / total_students) * 100
                
                attendance_data.append({
                    'classID': class_id,
                    'attendanceRate': round(attendance_rate, 2),
                    'totalStudents': total_students,
                    'attendedStudents': attended_students
                })
            
            return Response(attendance_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving attendance status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetEmotionsStatus(APIView):
    """
    API endpoint to get emotions distribution of all classes as a list
    """
    
    def get(self, request):
        """
        Get emotions distribution for all classes
        
        Returns:
            Response: List of emotions distribution for all classes
        """
        try:
            # Get all unique class IDs
            class_ids = StudentData.objects.values_list('ClassID', flat=True).distinct()
            
            emotions_data = []
            for class_id in class_ids:
                # Get all records for this class
                class_records = StudentData.objects.filter(ClassID=class_id)
                
                # Aggregate emotion distribution across all students in class
                emotion_distribution = {}
                for record in class_records:
                    if isinstance(record.Emotion, dict):
                        for emotion, value in record.Emotion.items():
                            if emotion in emotion_distribution:
                                emotion_distribution[emotion] += value
                            else:
                                emotion_distribution[emotion] = value
                
                emotions_data.append({
                    'classID': class_id,
                    'emotionDistribution': emotion_distribution
                })
            
            return Response(emotions_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving emotions status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetStudentOverallStatus(APIView):
    """
    API endpoint to get a list of how many classes each student attended
    """
    
    def get(self, request):
        """
        Get overall attendance status for all students
        
        Returns:
            Response: List of student attendance data
        """
        try:
            # Get all unique student IDs
            student_ids = StudentData.objects.values_list('studentID', flat=True).distinct()
            
            total_classes = StudentData.objects.values('ClassID').distinct().count()
            
            student_data = []
            for student_id in student_ids:
                # Get all records for this student
                student_records = StudentData.objects.filter(studentID=student_id)
                
                # Count unique classes attended
                classes_attended = student_records.values('ClassID').distinct().count()
                
                
                student_data.append({
                    'studentID': student_id,
                    'classesAttended': classes_attended,
                    'totalClasses': total_classes
                })
            
            return Response(student_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving student overall status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetStudentsDetailStatus(APIView):
    """
    API endpoint to get detailed status for all students
    Returns a map where key is student name and value is overallAttendance, classMentioned and class breakdown data
    """
    
    def get(self, request):
        """
        Get detailed status for all students
        
        Returns:
            Response: Map of student details with attendance and class breakdown
        """
        try:
            # Get all unique student IDs
            student_ids = StudentData.objects.values_list('studentID', flat=True).distinct()
            
            total_classes = StudentData.objects.values('ClassID').distinct().count()
            
            students_detail = {}
            for student_id in student_ids:
                # Get all records for this student
                student_records = StudentData.objects.filter(studentID=student_id)
                
                # Calculate overall attendance
                classes_attended = student_records.values('ClassID').distinct().count()
                
                # Get class breakdown data
                class_breakdown = {}
                unique_classes = student_records.values('ClassID').distinct()
                
                for class_data in unique_classes:
                    class_id = class_data['ClassID']
                    class_records = student_records.filter(ClassID=class_id, studentID=student_id)
                    
                    # Calculate emotion summary for this class
                    emotion_summary = {}
                    for record in class_records:
                        if isinstance(record.Emotion, dict):
                            for emotion, value in record.Emotion.items():
                                if emotion in emotion_summary:
                                    emotion_summary[emotion] += value
                                else:
                                    emotion_summary[emotion] = value
                    
                    class_breakdown[class_id] = {
                        'framesAttended': class_records.count(),
                        'emotionSummary': emotion_summary
                    }
                
                students_detail[student_id] = {
                    'overallAttendance': {
                        'overallAttendance': round(classes_attended / total_classes, 2),
                        'classesAttended': classes_attended
                    },
                    'classMentioned': list(class_breakdown.keys()),
                    'classBreakdown': class_breakdown
                }
            
            return Response(students_detail, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving students detail status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetClassDetailStatus(APIView):
    """
    API endpoint to get detailed status for all classes
    Returns a map where key is classID and value is attendance rate, present students, emotion distribution and student breakdown
    """
    
    def get(self, request):
        """
        Get detailed status for all classes
        
        Returns:
            Response: Map of class details with attendance, emotions and student breakdown
        """
        try:
            # Get all unique class IDs
            class_ids = StudentData.objects.values_list('ClassID', flat=True).distinct()
            
            total_students = StudentData.objects.values('studentID').distinct().count()
            
            class_detail = {}
            for class_id in class_ids:
                # Get all records for this class
                class_records = StudentData.objects.filter(ClassID=class_id)
                
                # Get unique students in this class
                unique_students_in_class = class_records.values('studentID').distinct()
                total_students_in_class = unique_students_in_class.count()
                
                # Calculate attendance rate
                attendance_rate = 0.0
                if total_students > 0:
                    # Count students who have any records (attended)
                    attended_students = total_students_in_class
                    attendance_rate = (attended_students / total_students) * 100
                
                # Aggregate emotion distribution across all students in class
                emotion_distribution = {}
                for record in class_records:
                    if isinstance(record.Emotion, dict):
                        for emotion, value in record.Emotion.items():
                            if emotion in emotion_distribution:
                                emotion_distribution[emotion] += value
                            else:
                                emotion_distribution[emotion] = value
                
                # Get student breakdown data
                student_breakdown = {}
                for student_data in unique_students_in_class:
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
                    
                    student_breakdown[student_id] = {
                        'framesAttended': student_records.count(),
                        'emotionSummary': student_emotion_summary
                    }
                
                class_detail[class_id] = {
                    'attendanceRate': round(attendance_rate, 2),
                    'presentStudents': total_students,
                    'emotionDistribution': emotion_distribution,
                    'studentBreakdown': student_breakdown
                }
            
            return Response(class_detail, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error retrieving class detail status: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

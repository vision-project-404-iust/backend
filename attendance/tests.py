from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import StudentData


class StudentDataModelTest(TestCase):
    """Test cases for StudentData model"""
    
    def setUp(self):
        """Set up test data"""
        self.student_data = StudentData.objects.create(
            studentID="STU001",
            FramID=1,
            ClassID=101,
            Emotion={"happy": 0.8, "sad": 0.1, "neutral": 0.1}
        )
    
    def test_student_data_creation(self):
        """Test that StudentData can be created"""
        self.assertEqual(self.student_data.studentID, "STU001")
        self.assertEqual(self.student_data.FramID, 1)
        self.assertEqual(self.student_data.ClassID, 101)
        self.assertEqual(self.student_data.Emotion["happy"], 0.8)
    
    def test_string_representation(self):
        """Test the string representation of StudentData"""
        expected = "Student STU001 - Class 101 - Frame 1"
        self.assertEqual(str(self.student_data), expected)


class AttendanceAPITest(APITestCase):
    """Test cases for Attendance API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        # Create multiple test records
        StudentData.objects.create(
            studentID="STU001",
            FramID=1,
            ClassID=101,
            Emotion={"happy": 0.8, "sad": 0.1, "neutral": 0.1}
        )
        StudentData.objects.create(
            studentID="STU002",
            FramID=1,
            ClassID=101,
            Emotion={"happy": 0.6, "sad": 0.3, "neutral": 0.1}
        )
        StudentData.objects.create(
            studentID="STU001",
            FramID=2,
            ClassID=102,
            Emotion={"happy": 0.7, "sad": 0.2, "neutral": 0.1}
        )
    
    def test_get_attendance_status(self):
        """Test GetAttendanceStatus API endpoint"""
        url = reverse('attendance:attendance-status')
        response = self.client.get(url)
        
        # Should return 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)  # 2 classes
        
        # Check first class data
        first_class = response.data[0]
        self.assertIn('classID', first_class)
        self.assertIn('attendanceRate', first_class)
        self.assertIn('totalStudents', first_class)
    
    def test_get_emotions_status(self):
        """Test GetEmotionsStatus API endpoint"""
        url = reverse('attendance:emotions-status')
        response = self.client.get(url)
        
        # Should return 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)  # 2 classes
        
        # Check first class data
        first_class = response.data[0]
        self.assertIn('classID', first_class)
        self.assertIn('emotionDistribution', first_class)
    
    def test_get_student_overall_status(self):
        """Test GetStudentOverallStatus API endpoint"""
        url = reverse('attendance:student-overall-status')
        response = self.client.get(url)
        
        # Should return 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)  # 2 students
        
        # Check first student data
        first_student = response.data[0]
        self.assertIn('studentID', first_student)
        self.assertIn('classesAttended', first_student)
        self.assertIn('totalClasses', first_student)
    
    def test_get_students_detail_status(self):
        """Test GetStudentsDetailStatus API endpoint"""
        url = reverse('attendance:students-detail-status')
        response = self.client.get(url)
        
        # Should return 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(len(response.data), 2)  # 2 students
        
        # Check first student data
        first_student_id = list(response.data.keys())[0]
        first_student_data = response.data[first_student_id]
        self.assertIn('overallAttendance', first_student_data)
        self.assertIn('classMentioned', first_student_data)
        self.assertIn('classBreakdown', first_student_data)
    
    def test_get_class_detail_status(self):
        """Test GetClassDetailStatus API endpoint"""
        url = reverse('attendance:class-detail-status')
        response = self.client.get(url)
        
        # Should return 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(len(response.data), 2)  # 2 classes
        
        # Check first class data
        first_class_id = list(response.data.keys())[0]
        first_class_data = response.data[first_class_id]
        self.assertIn('attendanceRate', first_class_data)
        self.assertIn('presentStudents', first_class_data)
        self.assertIn('emotionDistribution', first_class_data)
        self.assertIn('studentBreakdown', first_class_data)
    



class URLPatternsTest(TestCase):
    """Test cases for URL patterns"""
    
    def test_attendance_status_url(self):
        """Test attendance status URL pattern"""
        url = reverse('attendance:attendance-status')
        self.assertEqual(url, '/api/attendance-status/')
    
    def test_emotions_status_url(self):
        """Test emotions status URL pattern"""
        url = reverse('attendance:emotions-status')
        self.assertEqual(url, '/api/emotions-status/')
    
    def test_student_overall_status_url(self):
        """Test student overall status URL pattern"""
        url = reverse('attendance:student-overall-status')
        self.assertEqual(url, '/api/student-overall-status/')
    
    def test_students_detail_status_url(self):
        """Test students detail status URL pattern"""
        url = reverse('attendance:students-detail-status')
        self.assertEqual(url, '/api/students-detail-status/')
    
    def test_class_detail_status_url(self):
        """Test class detail status URL pattern"""
        url = reverse('attendance:class-detail-status')
        self.assertEqual(url, '/api/class-detail-status/')
    


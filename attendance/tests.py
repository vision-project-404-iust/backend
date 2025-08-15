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
        self.student_data = StudentData.objects.create(
            studentID="STU001",
            FramID=1,
            ClassID=101,
            Emotion={"happy": 0.8, "sad": 0.1, "neutral": 0.1}
        )
    
    def test_get_student_overall_status(self):
        """Test GetStudentOverallStatus API endpoint"""
        url = reverse('attendance:student-overall-status', args=['STU001'])
        response = self.client.get(url)
        
        # Should return 200 OK with placeholder data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('studentID', response.data)
        self.assertIn('overall_status', response.data)
    
    def test_get_class_status(self):
        """Test GetClassStatus API endpoint"""
        url = reverse('attendance:class-status', args=[101])
        response = self.client.get(url)
        
        # Should return 200 OK with placeholder data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ClassID', response.data)
        self.assertIn('total_students', response.data)
    
    def test_student_list(self):
        """Test StudentDataList API endpoint"""
        url = reverse('attendance:student-list')
        response = self.client.get(url)
        
        # Should return 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_student_detail(self):
        """Test StudentDataDetail API endpoint"""
        url = reverse('attendance:student-detail', args=[self.student_data.id])
        response = self.client.get(url)
        
        # Should return 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['studentID'], 'STU001')


class URLPatternsTest(TestCase):
    """Test cases for URL patterns"""
    
    def test_student_status_url(self):
        """Test student status URL pattern"""
        url = reverse('attendance:student-overall-status', args=['STU001'])
        self.assertEqual(url, '/api/student/STU001/status/')
    
    def test_class_status_url(self):
        """Test class status URL pattern"""
        url = reverse('attendance:class-status', args=[101])
        self.assertEqual(url, '/api/class/101/status/')
    
    def test_add_class_data_url(self):
        """Test add class data URL pattern"""
        url = reverse('attendance:add-class-data')
        self.assertEqual(url, '/api/class/add-data/')

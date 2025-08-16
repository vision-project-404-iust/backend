from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Main API endpoints
    path('attendance-status/', views.GetAttendanceStatus.as_view(), name='attendance-status'),
    path('emotions-status/', views.GetEmotionsStatus.as_view(), name='emotions-status'),
    path('student-overall-status/', views.GetStudentOverallStatus.as_view(), name='student-overall-status'),
    path('students-detail-status/', views.GetStudentsDetailStatus.as_view(), name='students-detail-status'),
    path('class-detail-status/', views.GetClassDetailStatus.as_view(), name='class-detail-status'),
    
    # Development/testing endpoints
    path('students/', views.StudentDataList.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDataDetail.as_view(), name='student-detail'),
]

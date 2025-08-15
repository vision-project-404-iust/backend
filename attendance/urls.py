from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Main API endpoints
    path('student/<str:student_id>/status/', views.GetStudentOverallStatus.as_view(), name='student-overall-status'),
    path('class/<int:class_id>/status/', views.GetClassStatus.as_view(), name='class-status'),
    
    # Development/testing endpoints
    path('students/', views.StudentDataList.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDataDetail.as_view(), name='student-detail'),
]

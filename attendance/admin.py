from django.contrib import admin
from .models import StudentData


@admin.register(StudentData)
class StudentDataAdmin(admin.ModelAdmin):
    """
    Admin interface for StudentData model
    """
    list_display = ('studentID', 'ClassID', 'FramID', 'created_at', 'updated_at')
    list_filter = ('ClassID', 'studentID', 'created_at')
    search_fields = ('studentID', 'ClassID')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Student Information', {
            'fields': ('studentID', 'ClassID', 'FramID')
        }),
        ('Emotion Data', {
            'fields': ('Emotion',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset for admin"""
        return super().get_queryset(request).select_related()

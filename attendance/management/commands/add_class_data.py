from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import cv2
import json
from attendance.models import StudentData
from datetime import datetime


class Command(BaseCommand):
    """
    Django management command to process video and add class data
    
    Usage:
        python manage.py add_class_data <video_path> [--class-id CLASS_ID] [--frame-interval FRAME_INTERVAL]
    
    Example:
        python manage.py add_class_data /path/to/video.mp4 --class-id 101 --frame-interval 30
    """
    
    help = 'Process video file and add class attendance and emotion data'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'video_path',
            type=str,
            help='Path to the video file to process'
        )
        parser.add_argument(
            '--class-id',
            type=int,
            default=1,
            help='Class ID for the video (default: 1)'
        )
        parser.add_argument(
            '--frame-interval',
            type=int,
            default=30,
            help='Process every Nth frame (default: 30)'
        )
    
    def handle(self, *args, **options):
        video_path = options['video_path']
        class_id = options['class_id']
        frame_interval = options['frame_interval']
        
        # Validate video file exists
        if not os.path.exists(video_path):
            raise CommandError(f'Video file not found: {video_path}')
                
        self.stdout.write(
            self.style.SUCCESS(f'Processing video: {video_path}')
        )
        self.stdout.write(f'Class ID: {class_id}')
        self.stdout.write(f'Frame interval: {frame_interval}')
        
    
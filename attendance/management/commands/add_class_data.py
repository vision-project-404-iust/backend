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
        parser.add_argument(
            '--output-dir',
            type=str,
            help='Directory to save processed frames (optional)'
        )
    
    def handle(self, *args, **options):
        video_path = options['video_path']
        class_id = options['class_id']
        frame_interval = options['frame_interval']
        output_dir = options['output_dir']
        
        # Validate video file exists
        if not os.path.exists(video_path):
            raise CommandError(f'Video file not found: {video_path}')
        
        if not os.path.isfile(video_path):
            raise CommandError(f'Path is not a file: {video_path}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Processing video: {video_path}')
        )
        self.stdout.write(f'Class ID: {class_id}')
        self.stdout.write(f'Frame interval: {frame_interval}')
        
        try:
            # Process the video
            processed_data = self.process_video(
                video_path, 
                class_id, 
                frame_interval, 
                output_dir
            )
            
            # Save to database
            self.save_to_database(processed_data)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully processed video and saved {len(processed_data)} records'
                )
            )
            
        except Exception as e:
            raise CommandError(f'Error processing video: {str(e)}')
    
    def process_video(self, video_path, class_id, frame_interval, output_dir):
        """
        Process video file and extract student data
        
        Args:
            video_path (str): Path to video file
            class_id (int): Class identifier
            frame_interval (int): Process every Nth frame
            output_dir (str): Optional directory to save frames
            
        Returns:
            list: List of dictionaries containing student data
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise CommandError(f'Could not open video file: {video_path}')
        
        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        self.stdout.write(f'Video info: {total_frames} frames, {fps:.2f} FPS, {duration:.2f}s duration')
        
        processed_data = []
        frame_count = 0
        processed_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Process every Nth frame
                if frame_count % frame_interval == 0:
                    self.stdout.write(f'Processing frame {frame_count}/{total_frames}')
                    
                    # TODO: Implement actual student detection and emotion analysis
                    # This is a placeholder implementation
                    student_data = self.analyze_frame(frame, frame_count, class_id)
                    
                    if student_data:
                        processed_data.extend(student_data)
                        processed_count += 1
                    
                    # Save frame if output directory specified
                    if output_dir and os.path.exists(output_dir):
                        frame_filename = f'frame_{frame_count:06d}.jpg'
                        frame_path = os.path.join(output_dir, frame_filename)
                        cv2.imwrite(frame_path, frame)
        
        finally:
            cap.release()
        
        self.stdout.write(f'Processed {processed_count} frames out of {total_frames} total frames')
        return processed_data
    
    def analyze_frame(self, frame, frame_id, class_id):
        """
        Analyze a single frame for student detection and emotion analysis
        
        Args:
            frame: OpenCV frame object
            frame_id (int): Frame number
            class_id (int): Class identifier
            
        Returns:
            list: List of student data dictionaries
        """
        # TODO: Implement actual computer vision logic here
        # This should include:
        # - Face detection
        # - Student identification
        # - Emotion recognition
        # - Attendance tracking
        
        # Placeholder implementation - replace with actual CV logic
        student_data = []
        
        # Simulate detecting 3 students in the frame
        for i in range(3):
            student_record = {
                'studentID': f'STU{frame_id:06d}_{i+1:02d}',
                'FramID': frame_id,
                'ClassID': class_id,
                'Emotion': {
                    'primary_emotion': 'neutral',
                    'confidence': 0.85,
                    'emotions': {
                        'happy': 0.1,
                        'sad': 0.05,
                        'angry': 0.0,
                        'surprised': 0.0,
                        'neutral': 0.85
                    }
                }
            }
            student_data.append(student_record)
        
        return student_data
    
    def save_to_database(self, processed_data):
        """
        Save processed student data to database
        
        Args:
            processed_data (list): List of student data dictionaries
        """
        if not processed_data:
            self.stdout.write(self.style.WARNING('No data to save'))
            return
        
        # Convert to StudentData objects
        student_objects = []
        for data in processed_data:
            student_obj = StudentData(
                studentID=data['studentID'],
                FramID=data['FramID'],
                ClassID=data['ClassID'],
                Emotion=data['Emotion']
            )
            student_objects.append(student_obj)
        
        # Bulk create records
        created_records = StudentData.objects.bulk_create(student_objects)
        
        self.stdout.write(
            self.style.SUCCESS(f'Created {len(created_records)} database records')
        )

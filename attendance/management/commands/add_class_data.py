from math import inf
from django.core.management.base import BaseCommand, CommandError
import os
from attendance.models import StudentData
from typing import List, Tuple
from ultralytics import YOLO
from deepface import DeepFace
import cv2

TRACK_MODEL_PATH = "attendance/management/commands/yolov8n-face-lindevs.onnx"
DB_PATH = "attendance/management/commands/db"

class Command(BaseCommand):
    """
    Django management command to process video and add class data
    
    Usage:
        python manage.py add_class_data <video_path> [--class-id CLASS_ID] [--frame-interval FRAME_INTERVAL]
    
    Example:
        python manage.py add_class_data /path/to/video.mp4 --class-id 101 --frame-interval 100
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
            default=500,
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
        
        
        self.track_model = self.get_track_model()
        
        track_id_matches = {}
        
        data_set = []
        
        for frame_id, frame in enumerate(self.get_frames(video_path, frame_interval)):
            if frame_id % 5 == 0:
                self.stdout.write(f'Processing frame {frame_id}')

            for track_id, box in self.get_boxes(frame):
                if track_id not in track_id_matches:
                    track_id_matches[track_id] = {}
                
                emotions : List[Tuple[str, float]] = self.get_emotion(box, frame)
                
                data_set.append((track_id, frame_id, emotions))
                
                top_match : List[Tuple[str, float]] = self.get_top_match(box, frame)

                for match, distance in top_match:
                    track_id_matches[track_id].setdefault(match, []).append(distance)

        track_student_mapping = self.get_track_id_student_mapping(track_id_matches)

        for track_id, frame_id, emotions in data_set:
            student = track_student_mapping[track_id]
            
            if StudentData.objects.filter(studentID=student, ClassID=class_id, FramID=frame_id).exists():
                continue
            
            StudentData.objects.create(
                studentID=student,
                ClassID=class_id,
                FramID=frame_id,
                Emotion=emotions
            )
        
        self.stdout.write(self.style.SUCCESS(f'Added {len(data_set)} data points'))

    def download_yolo_model(self):
        import requests
        link = "https://github.com/lindevs/yolov8-face/releases/latest/download/yolov8n-face-lindevs.onnx"
        
        if not os.path.exists(TRACK_MODEL_PATH):
            response = requests.get(link)
            with open(TRACK_MODEL_PATH, "wb") as f:
                f.write(response.content)

        
    def get_track_model(self):
        self.download_yolo_model()
        
        return YOLO(TRACK_MODEL_PATH)


    def get_frames(self, video_path, frame_interval):
        cap = cv2.VideoCapture(video_path)
        frame_id = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_id % frame_interval == 0:
                yield frame
            frame_id += 1
        cap.release()
    
    def get_boxes(self, frame):
        results = self.track_model.track(frame, persist=True, classes=[0])
        result = results[0]

        boxes = result.boxes.xywh.cpu().numpy().astype(int).tolist()
        track_ids = result.boxes.id.cpu().numpy().astype(int).tolist()

        return zip(track_ids, boxes)

    
    def get_emotion(self, box, frame):
        x, y, w, h = box

        x1 = max(x - w // 2, 0)
        y1 = max(y - h // 2, 0)
        x2 = min(x + w // 2, frame.shape[1])
        y2 = min(y + h // 2, frame.shape[0])
        face_crop = frame[y1:y2, x1:x2]
        
        analysis = DeepFace.analyze(face_crop, actions=['emotion'], enforce_detection=False)

        emotions = analysis[0]['emotion']
        
        emotions_dict = {}
        
        for emotion, value in emotions.items():
            emotions_dict[emotion] = float(value)   
        
        return emotions_dict


    def get_top_match(self, box, frame):
        x, y, w, h = box

        x1 = max(x - w // 2, 0)
        y1 = max(y - h // 2, 0)
        x2 = min(x + w // 2, frame.shape[1])
        y2 = min(y + h // 2, frame.shape[0])
        face_crop = frame[y1:y2, x1:x2]
        
        df_find = DeepFace.find(
                img_path=face_crop,
                db_path=DB_PATH,
                detector_backend="mtcnn",
                model_name="ArcFace",
                enforce_detection=False,
                silent=True
        )
            
        df = df_find[0]
        df = df.head(3)
        
        top_match = []
        
        for _, match in df.iterrows():
            matched_img_path = match['identity']
            matched_img_path = matched_img_path.split('/')[-2]
            
            distance = match['distance']

            top_match.append((matched_img_path, distance))

        return top_match
        
    def get_track_id_student_mapping(self, track_id_matches):
        track_student_mapping = {}
        
        for track_id, students_distacne in track_id_matches.items():
            best_student = ""
            best_count = 0
            best_avg = inf
            for student, distance_list in students_distacne.items():
                count = len(distance_list)
                avg = sum(distance_list) / count
                
                if best_student == "" or count > best_count or (count == best_student and avg < best_avg):
                    best_student = student
                    best_count = count
                    best_avg = avg
            
            track_student_mapping[track_id] = student
        return track_student_mapping

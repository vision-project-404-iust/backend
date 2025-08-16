# Classroom Attendance System Backend

A Django-based backend system for managing classroom attendance with emotion tracking capabilities.

## Features

- **Student Data Management**: Store and manage student attendance records with emotion data
- **Attendance Tracking**: Track student attendance across different classes
- **Emotion Analysis**: Store and analyze emotion data in JSON format
- **RESTful APIs**: Clean API endpoints for data retrieval and management
- **PostgreSQL Database**: Robust database backend for production use

## Project Structure

```
backend/
├── attendance_system/          # Main Django project
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI application
│   └── asgi.py               # ASGI application
├── attendance/                # Attendance app
│   ├── __init__.py
│   ├── models.py             # StudentData model
│   ├── views.py              # API views
│   ├── serializers.py        # Data serializers
│   ├── urls.py               # App URL patterns
│   └── admin.py              # Admin interface
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── config.env.example         # Environment configuration template
```

## Database Schema

### StudentData Table
- `id`: Primary key (auto-increment)
- `studentID`: Student identifier (string)
- `FramID`: Frame identifier (integer)
- `ClassID`: Class identifier (integer)
- `Emotion`: Emotion data (JSON)
- `created_at`: Record creation timestamp
- `updated_at`: Record update timestamp

## API Endpoints

All API endpoints are prefixed with `/api/`

### Core APIs

#### 1. GetAttendanceStatus
**URL:** `/api/attendance-status/`  
**Method:** GET  
**Description:** Returns attendance rate of all classIDs as a list  
**Response Format:**
```json
[
  {
    "classID": 101,
    "attendanceRate": 85.5,
    "totalStudents": 20,
    "attendedStudents": 17
  },
  {
    "classID": 102,
    "attendanceRate": 92.0,
    "totalStudents": 15,
    "attendedStudents": 15
  }
]
```

#### 2. GetEmotionsStatus
**URL:** `/api/emotions-status/`  
**Method:** GET  
**Description:** Returns emotions distribution of all classes as a list  
**Response Format:**
```json
[
  {
    "classID": 101,
    "emotionDistribution": {
      "happy": 15.2,
      "sad": 3.1,
      "neutral": 8.7
    }
  },
  {
    "classID": 102,
    "emotionDistribution": {
      "happy": 12.5,
      "excited": 5.3,
      "neutral": 4.2
    }
  }
]
```

#### 3. GetStudentOverallStatus
**URL:** `/api/student-overall-status/`  
**Method:** GET  
**Description:** Returns a list of how many classes each student attended  
**Response Format:**
```json
[
  {
    "studentID": "STU001",
    "classesAttended": 3,
    "totalClasses": 25
  },
  {
    "studentID": "STU002",
    "classesAttended": 2,
    "totalClasses": 18
  }
]
```

#### 4. GetStudentsDetailStatus
**URL:** `/api/students-detail-status/`  
**Method:** GET  
**Description:** Returns a map where the key is student name and the value is overallAttendance, classMentioned and class breakdown data  
**Response Format:**
```json
{
  "STU001": {
    "overallAttendance": {
      "overallAttendance": 0.92,
      "classesAttended": 25
    },
    "classMentioned": [101, 102, 103],
    "classBreakdown": {
      "101": {
        "framesAttended": 10,
        "emotionSummary": {
          "happy": 8.5,
          "neutral": 1.5
        }
      },
      "102": {
        "framesAttended": 8,
        "emotionSummary": {
          "happy": 6.2,
          "sad": 1.8
        }
      }
    }
  }
}
```

#### 5. GetClassDetailStatus
**URL:** `/api/class-detail-status/`  
**Method:** GET  
**Description:** Returns a map where the key is the classID and the value is attendance rate, present students, emotion distribution and student breakdown  
**Response Format:**
```json
{
  "101": {
    "attendanceRate": 85.5,
    "presentStudents": 17,
    "emotionDistribution": {
      "happy": 15.2,
      "sad": 3.1,
      "neutral": 8.7
    },
    "studentBreakdown": {
      "STU001": {
        "framesAttended": 10,
        "emotionSummary": {
          "happy": 8.5,
          "neutral": 1.5
        }
      },
      "STU002": {
        "framesAttended": 7,
        "emotionSummary": {
          "happy": 6.7,
          "sad": 0.3
        }
      }
    }
  }
}
```

### Development/Testing APIs
- `GET /api/students/` - List all student records
- `GET /api/students/{id}/` - Get specific student record

## Data Model Notes

- All attendance calculations are based on the presence of student records in the database
- Emotion data is aggregated across all frames for each student/class
- Attendance rates are calculated as percentages (0-100)
- The system assumes that if a student has records for a class, they attended that class

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### 2. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb attendance_db

# Copy environment configuration
cp config.env.example .env

# Edit .env file with your database credentials
# Update DB_PASSWORD and other settings as needed
```

### 4. Django Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 5. Verify Installation
- Access admin interface: http://localhost:8000/admin/
- API base URL: http://localhost:8000/api/

## Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: PostgreSQL host
- `DB_PORT`: PostgreSQL port

## Development

### Adding New Features
1. Create models in `attendance/models.py`
2. Add serializers in `attendance/serializers.py`
3. Implement views in `attendance/views.py`
4. Update URL patterns in `attendance/urls.py`
5. Run tests and migrations

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Include type hints where appropriate

## Video Processing Pipeline

The system includes a powerful video processing pipeline that automatically extracts attendance and emotion data from classroom videos.

### add_class_data Command

The `add_class_data` command is a Django management command that processes video files and populates the database with student attendance and emotion data.

#### Usage
```bash
python manage.py add_class_data <video_path> [--class-id CLASS_ID] [--frame-interval FRAME_INTERVAL]
```

#### Parameters
- `video_path`: Path to the video file to process
- `--class-id`: Class ID for the video (default: 1)
- `--frame-interval`: Process every Nth frame (default: 30)

#### Example
```bash
python manage.py add_class_data /path/to/classroom_video.mp4 --class-id 101 --frame-interval 30
```

#### How It Works

1. **Video Processing**: The command reads the video file and extracts frames at specified intervals
2. **Face Detection**: Uses YOLOv8 face detection model to identify faces in each frame
3. **Face Tracking**: Tracks individual faces across frames using unique track IDs
4. **Emotion Analysis**: Analyzes each detected face using DeepFace to extract emotion data
5. **Student Recognition**: Matches detected faces against a database of known student faces
6. **Data Population**: Creates StudentData records with:
   - Student ID (from face recognition)
   - Class ID (specified parameter)
   - Frame ID (sequential frame number)
   - Emotion data (JSON format with emotion scores)

#### Requirements

The command requires the following models and dependencies:
- **YOLOv8 Face Detection Model**: `models/yolov8n-face-lindevs.onnx`
- **Student Face Database**: `models/db/` directory containing known student face images
- **DeepFace**: For emotion analysis and face recognition
- **OpenCV**: For video processing

#### Output

The command processes the entire video and creates multiple `StudentData` records, one for each detected face in each processed frame. This data is then available through the API endpoints for attendance tracking and emotion analysis.

## Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Production Considerations
- Set `DEBUG=False`
- Use environment variables for sensitive data
- Configure proper database credentials
- Set up static file serving
- Configure HTTPS
- Set up proper logging

### Docker (Optional)
```bash
# Build and run with Docker
docker build -t attendance-system .
docker run -p 8000:8000 attendance-system
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

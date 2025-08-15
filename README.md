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

### Core APIs
- `GET /api/student/{student_id}/status/` - Get student overall status
- `GET /api/class/{class_id}/status/` - Get class attendance status
- `POST /api/class/add-data/` - Add class data pipeline

### Development APIs
- `GET /api/students/` - List all student records
- `GET /api/students/{id}/` - Get specific student record

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

## TODO Implementation

The following features are marked for future implementation:

### GetStudentOverallStatus API
- Calculate total classes vs attended classes
- Compute overall attendance rate
- Aggregate emotion data across classes
- Determine overall status (Excellent/Good/Fair/Poor)

### GetClassStatus API
- Count total students in class
- Calculate present vs absent students
- Compute class attendance rate
- Aggregate emotion distribution
- Generate student status list

### Class Data Pipeline
- Process incoming class data
- Handle multiple student records
- Validate data integrity
- Implement bulk insertion
- Process emotion data

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
